from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, filters, status
from .models import Category, Post, Comment
from .serializers import CategorySerializer, PostSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from django.db.models import Q, Count, Prefetch
from django.utils.text import slugify
from django.utils import timezone
from datetime import timedelta
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
import json
import os

# Create your views here.

class IsAuthorOrReadOnly(IsAuthenticatedOrReadOnly):
    """
    작성자만 수정/삭제할 수 있는 권한 클래스
    """
    def has_object_permission(self, request, view, obj):
        # 읽기 권한은 모든 요청에 허용
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        
        # 작성자만 수정/삭제 권한 허용
        return obj.author == request.user

# 캐시 적용된 카테고리 조회
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
    
    @method_decorator(cache_page(60 * 15))  # 15분 캐싱
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @method_decorator(cache_page(60 * 15))  # 15분 캐싱
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

# 캐시 적용된 포스트 조회
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'title']
    
    def get_queryset(self):
        """
        사용자 상태에 따라 다른 쿼리셋 반환
        인증된 사용자가 자신의 글을 요청하는 경우 (my_posts) 모든 글 반환
        그 외에는 published=True인 글만 반환
        """
        queryset = Post.objects.all()
        
        # 성능 최적화: select_related로 author와 category 미리 로드
        queryset = queryset.select_related('author', 'category')
        
        # 성능 최적화: prefetch_related로 댓글 미리 로드
        queryset = queryset.prefetch_related(
            Prefetch(
                'comments',
                queryset=Comment.objects.filter(parent=None, is_approved=True).select_related('author')
            )
        )
            
        # 기본적으로는 공개된 글만 보이도록 설정
        if self.action != 'my_posts':
            queryset = queryset.filter(is_published=True)
            
        # 카테고리 필터링
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category__slug=category)
            
        return queryset
    
    @method_decorator(cache_page(60 * 5))  # 5분 캐싱
    def list(self, request, *args, **kwargs):
        # 인증된 사용자인 경우 캐싱하지 않음
        if request.user.is_authenticated:
            return super().list(request, *args, **kwargs)
        return super().list(request, *args, **kwargs)
    
    @method_decorator(cache_page(60 * 5))  # 5분 캐싱
    def retrieve(self, request, *args, **kwargs):
        # 인증된 사용자인 경우 캐싱하지 않음
        if request.user.is_authenticated:
            return super().retrieve(request, *args, **kwargs)
        return super().retrieve(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        """
        글 작성 시 현재 사용자를 작성자로 설정
        """
        serializer.save(author=self.request.user)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_posts(self, request):
        """
        로그인한 사용자 자신의 모든 글 목록 반환 (비공개 글 포함)
        """
        posts = Post.objects.filter(author=request.user).select_related('author', 'category')
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def draft(self, request):
        """
        임시저장 기능: 글을 비공개로 저장
        """
        # 기존 serializer 사용하되 is_published를 False로 설정
        request.data['is_published'] = False
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_comment(self, request, slug=None):
        """
        글에 댓글 추가
        """
        post = self.get_object()
        
        # 요청 데이터에 post ID 추가
        data = request.data.copy()
        data['post'] = post.id
        
        # 부모 댓글 ID가 있는 경우 대댓글로 처리
        parent_id = data.get('parent', None)
        
        serializer = CommentSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]
    
    def get_queryset(self):
        queryset = Comment.objects.select_related('author', 'post', 'parent')
        
        # 글 ID로 필터링
        post_id = self.request.query_params.get('post', None)
        if post_id:
            queryset = queryset.filter(post_id=post_id)
            
        # 승인된 댓글만 반환 (인증된 사용자가 자신의 댓글을 요청하는 경우 예외)
        if not self.request.user.is_authenticated or self.action != 'my_comments':
            queryset = queryset.filter(is_approved=True)
            
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_comments(self, request):
        """
        로그인한 사용자 자신의 모든 댓글 목록 반환
        """
        comments = Comment.objects.filter(author=request.user).select_related('post', 'author')
        serializer = self.get_serializer(comments, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_stats(request):
    """
    블로그 통계 정보를 제공하는 API
    - 총 게시물 수
    - 카테고리 수
    - 댓글 수
    - 최근 활동 내역
    """
    # 통계 데이터 수집
    total_posts = Post.objects.filter(author=request.user).count()
    total_categories = Category.objects.count()
    total_comments = Comment.objects.filter(post__author=request.user).count()
    
    # 최근 활동 내역
    recent_activities = []
    
    # 최근 작성한 글
    recent_posts = Post.objects.filter(
        author=request.user
    ).order_by('-created_at')[:3]
    
    for post in recent_posts:
        time_diff = timezone.now() - post.created_at
        if time_diff < timedelta(minutes=10):
            time_str = '방금 전'
        elif time_diff < timedelta(hours=1):
            time_str = f'{int(time_diff.total_seconds() // 60)}분 전'
        elif time_diff < timedelta(days=1):
            time_str = f'{int(time_diff.total_seconds() // 3600)}시간 전'
        else:
            time_str = f'{int(time_diff.days)}일 전'
            
        activity = {
            'text': f'새 글 "{post.title}"을 작성했습니다.',
            'icon': 'fas fa-file-alt',
            'color': 'text-primary',
            'time': time_str
        }
        recent_activities.append(activity)
    
    # 최근 받은 댓글
    recent_comments = Comment.objects.filter(
        post__author=request.user
    ).select_related('post', 'author').order_by('-created_at')[:3]
    
    for comment in recent_comments:
        time_diff = timezone.now() - comment.created_at
        if time_diff < timedelta(minutes=10):
            time_str = '방금 전'
        elif time_diff < timedelta(hours=1):
            time_str = f'{int(time_diff.total_seconds() // 60)}분 전'
        elif time_diff < timedelta(days=1):
            time_str = f'{int(time_diff.total_seconds() // 3600)}시간 전'
        else:
            time_str = f'{int(time_diff.days)}일 전'
            
        activity = {
            'text': f'{comment.author.username}님이 "{comment.post.title}" 글에 댓글을 남겼습니다.',
            'icon': 'fas fa-comment',
            'color': 'text-success',
            'time': time_str
        }
        recent_activities.append(activity)
    
    # 활동 내역을 최신순으로 정렬
    recent_activities.sort(key=lambda x: x['time'], reverse=True)
    
    # 각 카테고리별 게시물 수
    category_stats = Category.objects.annotate(
        post_count=Count('post')
    ).values('id', 'name', 'slug', 'post_count')
    
    return Response({
        'stats': {
            'posts': total_posts,
            'categories': total_categories,
            'comments': total_comments
        },
        'recent_activities': recent_activities,
        'category_stats': list(category_stats)
    })

# 블로그 설정 JSON 파일 경로
def get_settings_file_path():
    """
    설정 파일 경로를 반환합니다.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, 'blog_settings.json')

@api_view(['GET'])
@cache_page(60 * 30)  # 30분 캐싱
def get_settings(request):
    """
    블로그 설정을 조회하는 API
    """
    try:
        with open(get_settings_file_path(), 'r', encoding='utf-8') as f:
            settings = json.load(f)
        return Response(settings)
    except Exception as e:
        return Response(
            {"error": f"설정을 불러오는 중 오류가 발생했습니다: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_settings(request):
    """
    블로그 설정을 업데이트하는 API
    """
    try:
        # 기존 설정 불러오기
        with open(get_settings_file_path(), 'r', encoding='utf-8') as f:
            settings = json.load(f)
        
        # 요청 데이터로 설정 업데이트
        for key, value in request.data.items():
            settings[key] = value
        
        # 업데이트된 설정 저장
        with open(get_settings_file_path(), 'w', encoding='utf-8') as f:
            json.dump(settings, f, ensure_ascii=False)
        
        return Response(settings)
    except Exception as e:
        return Response(
            {"error": f"설정을 업데이트하는 중 오류가 발생했습니다: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
