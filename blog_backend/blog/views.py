from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, filters, status
from .models import Category, Post, Comment
from .serializers import CategorySerializer, PostSerializer, CommentSerializer, UserProfileSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from django.db.models import Q, Count, Prefetch
from django.utils.text import slugify
from django.utils import timezone
from datetime import timedelta
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
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
    
    def get_queryset(self):
        """
        사용자별 카테고리만 반환하도록 쿼리셋 필터링
        """
        if self.request.user.is_authenticated:
            return Category.objects.filter(author=self.request.user)
        return Category.objects.none()
    
    def perform_create(self, serializer):
        """
        카테고리 생성 시 현재 사용자를 작성자로 설정
        """
        serializer.save(author=self.request.user)
    
    @method_decorator(cache_page(60 * 5))  # 5분 캐싱 (이전 15분)
    def list(self, request, *args, **kwargs):
        # 인증된 사용자는 캐시 사용 안함
        if request.user.is_authenticated:
            return super(CategoryViewSet, self).list(request, *args, **kwargs)
        return super().list(request, *args, **kwargs)
    
    @method_decorator(cache_page(60 * 5))  # 5분 캐싱 (이전 15분)
    def retrieve(self, request, *args, **kwargs):
        # 인증된 사용자는 캐시 사용 안함
        if request.user.is_authenticated:
            return super(CategoryViewSet, self).retrieve(request, *args, **kwargs)
        return super().retrieve(request, *args, **kwargs)
        
    def create(self, request, *args, **kwargs):
        """
        카테고리 생성 시 슬러그 처리를 위한 메소드 오버라이드
        """
        print("CategoryViewSet.create() 호출됨")
        print("요청 데이터:", request.data)
        
        # 슬러그가 없거나 빈 문자열인 경우 처리
        data = request.data.copy()  # 요청 데이터 복사 (변경 가능하도록)
        
        # 이름 필드 검증
        if not data.get('name'):
            return Response(
                {"name": "카테고리 이름은 필수입니다."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # 슬러그 자동 생성 (이미 있으면 유지)
        if not data.get('slug'):
            from django.utils.text import slugify
            import time
            
            name = data['name']
            base_slug = slugify(name)
            
            # 한글만 있는 경우 또는 슬러그가 비어있는 경우
            if not base_slug:
                base_slug = f"category-{int(time.time())}"
                
            # 슬러그 중복 방지
            slug = base_slug
            counter = 1
            
            while Category.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
                
            data['slug'] = slug
            print(f"슬러그 생성됨: {slug}")
        
        # 시리얼라이저 사용 및 생성
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

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
        else:
            # my_posts 액션인 경우 현재 사용자의 글만 반환
            queryset = queryset.filter(author=self.request.user)
            
        # 카테고리 필터링
        category = self.request.query_params.get('category', None)
        if category and self.request.user.is_authenticated:
            # 인증된 사용자인 경우 해당 사용자의 카테고리로 필터링
            queryset = queryset.filter(category__slug=category, category__author=self.request.user)
        elif category:
            # 비인증 사용자는 공개 글만 필터링
            queryset = queryset.filter(category__slug=category, is_published=True)
            
        return queryset
    
    @method_decorator(cache_page(60))  # 1분 캐싱으로 변경 (이전 5분)
    def list(self, request, *args, **kwargs):
        # 인증된 사용자인 경우 캐싱하지 않음 (명시적으로 처리)
        if request.user.is_authenticated:
            return super(PostViewSet, self).list(request, *args, **kwargs)
        return super().list(request, *args, **kwargs)
    
    @method_decorator(cache_page(60))  # 1분 캐싱으로 변경 (이전 5분)
    def retrieve(self, request, *args, **kwargs):
        # 인증된 사용자인 경우 캐싱하지 않음 (명시적으로 처리)
        if request.user.is_authenticated:
            return super(PostViewSet, self).retrieve(request, *args, **kwargs)
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
        print(f"my_posts 액션 호출: 사용자 {request.user.username}의 글 목록 요청")
        
        # 사용자 본인의 모든 게시물 조회 (최신순으로 정렬)
        posts = Post.objects.filter(author=request.user).select_related('author', 'category').order_by('-created_at')
        
        # 결과 로깅
        count = posts.count()
        print(f"조회된 게시물 수: {count}")
        if count > 0:
            print(f"첫 번째 게시물: ID={posts[0].id}, 제목='{posts[0].title}', 슬러그='{posts[0].slug}'")
        else:
            print("사용자의 게시물이 없습니다.")
        
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

    def destroy(self, request, *args, **kwargs):
        """
        게시물 삭제 시 더 자세한 오류 처리
        """
        try:
            # 로그 추가
            slug = kwargs.get('slug')
            print(f"게시물 삭제 시도: {slug}")
            
            # 게시물 존재 여부 확인
            try:
                instance = self.get_object()
            except Exception as e:
                print(f"게시물 조회 오류: {str(e)}")
                return Response(
                    {"error": f"삭제할 게시물을 찾을 수 없습니다. (slug: {slug})"},
                    status=status.HTTP_404_NOT_FOUND
                )
                
            # 권한 검사 (작성자만 삭제 가능)
            if instance.author != request.user:
                return Response(
                    {"error": "이 게시물을 삭제할 권한이 없습니다."},
                    status=status.HTTP_403_FORBIDDEN
                )
                
            # 실제 삭제 처리
            print(f"게시물 삭제 (ID: {instance.id}, 제목: {instance.title})")
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
            
        except Exception as e:
            print(f"게시물 삭제 중 예외 발생: {str(e)}")
            return Response(
                {"error": f"게시물 삭제 중 오류가 발생했습니다: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

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
    print(f"통계 API 호출: 사용자 {request.user.username}, 인증: {request.user.is_authenticated}")
    print(f"요청 헤더: {request.headers.get('Authorization', '헤더 없음')}")
    # 통계 데이터 수집
    total_posts = Post.objects.filter(author=request.user).count()
    # 사용자의 카테고리만 카운트하도록 수정
    total_categories = Category.objects.filter(author=request.user).count()
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
    
    # 각 카테고리별 게시물 수 - 사용자의 카테고리만 가져오도록 수정
    category_stats = Category.objects.filter(author=request.user).annotate(
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
@cache_page(60 * 5)  # 5분 캐싱 (이전 30분)
def get_settings(request):
    """
    블로그 설정을 조회하는 API
    """
    try:
        # 인증된 사용자인 경우 실시간 데이터 사용
        if request.user.is_authenticated:
            with open(get_settings_file_path(), 'r', encoding='utf-8') as f:
                settings = json.load(f)
            return Response(settings)
            
        # 비인증 사용자는 캐싱된 데이터 사용
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

# 사용자 프로필 API
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """
    사용자 프로필 조회 및 업데이트 API
    GET: 현재 로그인된 사용자의 프로필 정보 반환
    PUT: 프로필 정보 업데이트
    """
    user = request.user
    
    try:
        if request.method == 'GET':
            print(f"사용자 프로필 조회 요청: {user.username}")
            serializer = UserProfileSerializer(user)
            return Response(serializer.data)
        
        elif request.method == 'PUT':
            print(f"사용자 프로필 업데이트 요청: {user.username}, 데이터: {request.data}")
            serializer = UserProfileSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                print(f"사용자 프로필 업데이트 성공: {user.username}")
                return Response(serializer.data)
            print(f"사용자 프로필 업데이트 유효성 검사 실패: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(f"사용자 프로필 처리 중 오류 발생: {str(e)}")
        return Response(
            {"error": f"프로필 처리 중 오류가 발생했습니다: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# 비밀번호 재설정 토큰 생성
@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset(request):
    """
    비밀번호 재설정 이메일 전송 API
    - 이메일을 받아 해당 사용자에게 비밀번호 재설정 링크 전송
    """
    try:
        email = request.data.get('email')
        if not email:
            return Response(
                {"error": "이메일 주소를 입력해주세요."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # 사용자 존재 여부 확인
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # 보안을 위해 사용자가 없어도 성공 응답 반환 (이메일 존재 여부 노출 방지)
            return Response(
                {"message": "비밀번호 재설정 링크가 이메일로 전송되었습니다. 이메일을 확인해주세요."}
            )
        
        # 비밀번호 재설정 토큰 생성
        from django.contrib.auth.tokens import default_token_generator
        from django.utils.encoding import force_bytes
        from django.utils.http import urlsafe_base64_encode
        
        # 사용자 ID를 base64로 인코딩
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        # 토큰 생성
        token = default_token_generator.make_token(user)
        
        # 비밀번호 재설정 링크 생성
        from django.conf import settings
        reset_url = f"http://{settings.SITE_DOMAIN}/reset-password?uid={uid}&token={token}"
        
        # 이메일 전송
        from django.core.mail import send_mail
        
        subject = '[블로그] 비밀번호 재설정 안내'
        message = f"""
안녕하세요, {user.username}님.

회원님의 계정 비밀번호를 재설정하려면 아래 링크를 클릭해주세요:
{reset_url}

이 링크는 24시간 동안 유효합니다.
본인이 요청하지 않았다면 이 이메일을 무시하셔도 됩니다.

감사합니다.
블로그 관리자
        """
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER if hasattr(settings, 'EMAIL_HOST_USER') else None,
            recipient_list=[email],
            fail_silently=False
        )
        
        return Response(
            {"message": "비밀번호 재설정 링크가 이메일로 전송되었습니다. 이메일을 확인해주세요."}
        )
        
    except Exception as e:
        print(f"비밀번호 재설정 이메일 전송 중 오류: {str(e)}")
        return Response(
            {"error": "비밀번호 재설정 이메일 전송 중 오류가 발생했습니다."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# 비밀번호 재설정 확인
@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_confirm(request):
    """
    비밀번호 재설정 확인 API
    - uid, token, 새 비밀번호를 받아 비밀번호 변경 처리
    """
    try:
        uid = request.data.get('uid')
        token = request.data.get('token')
        new_password = request.data.get('new_password')
        
        if not uid or not token or not new_password:
            return Response(
                {"error": "모든 필드를 입력해주세요."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # UID 디코딩하여 사용자 찾기
        from django.utils.encoding import force_str
        from django.utils.http import urlsafe_base64_decode
        from django.contrib.auth.tokens import default_token_generator
        
        try:
            # UID 디코딩
            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response(
                {"error": "잘못된 비밀번호 재설정 링크입니다."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # 토큰 검증
        if not default_token_generator.check_token(user, token):
            return Response(
                {"error": "만료되었거나 유효하지 않은 비밀번호 재설정 링크입니다."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # 새 비밀번호 설정
        user.set_password(new_password)
        user.save()
        
        return Response(
            {"message": "비밀번호가 성공적으로 재설정되었습니다. 새 비밀번호로 로그인해주세요."}
        )
        
    except Exception as e:
        print(f"비밀번호 재설정 중 오류: {str(e)}")
        return Response(
            {"error": "비밀번호 재설정 중 오류가 발생했습니다."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
