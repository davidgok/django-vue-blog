from django.shortcuts import render
from rest_framework import viewsets, filters, status
from .models import Category, Post
from .serializers import CategorySerializer, PostSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from django.db.models import Q, Count
from django.utils.text import slugify
from django.utils import timezone
from datetime import timedelta

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

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

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
        
        # 기본적으로는 공개된 글만 보이도록 설정
        if self.action != 'my_posts':
            queryset = queryset.filter(is_published=True)
            
        # 카테고리 필터링
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category__slug=category)
            
        return queryset
    
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
        posts = Post.objects.filter(author=request.user)
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_stats(request):
    """
    블로그 통계 정보를 제공하는 API
    - 총 게시물 수
    - 카테고리 수
    - 댓글 수 (아직 미구현)
    - 최근 활동 내역
    """
    # 통계 데이터 수집
    total_posts = Post.objects.filter(author=request.user).count()
    total_categories = Category.objects.count()
    # 댓글 모델이 없으므로 임시로 0 반환
    total_comments = 0
    
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
