"""
URL configuration for blog_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from blog.views import CategoryViewSet, PostViewSet, CommentViewSet, get_stats, get_settings, update_settings
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib.auth import views as auth_views
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)

# 커스텀 토큰 인증 뷰
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
        })

# 회원가입 API
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    if 'username' not in request.data or 'password' not in request.data or 'email' not in request.data:
        return Response(
            {"error": "필수 필드가 누락되었습니다."},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    
    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "이미 존재하는 사용자 이름입니다."},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if User.objects.filter(email=email).exists():
        return Response(
            {"error": "이미 존재하는 이메일입니다."},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = User.objects.create_user(
        username=username, 
        password=password,
        email=email
    )
    
    token, created = Token.objects.get_or_create(user=user)
    
    return Response({
        "token": token.key,
        "username": user.username,
        "email": user.email
    }, status=status.HTTP_201_CREATED)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('api/auth/login/', CustomAuthToken.as_view(), name='api_token_auth'),
    path('api/auth/register/', register, name='register'),
    path('api/stats/', get_stats, name='blog_stats'),
    path('api/settings/', get_settings, name='get_settings'),
    path('api/settings/update/', update_settings, name='update_settings'),
    # 비밀번호 재설정 API는 더 복잡한 구현이 필요하므로 주석으로 처리
    # path('api/auth/password-reset/', password_reset, name='password_reset'),
    # path('api/auth/password-reset/confirm/', password_reset_confirm, name='password_reset_confirm'),
]
