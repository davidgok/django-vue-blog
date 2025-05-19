from rest_framework import serializers
from .models import Category, Post, Comment
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class UserProfileSerializer(serializers.ModelSerializer):
    """
    사용자 프로필 시리얼라이저
    """
    email = serializers.EmailField(read_only=True)  # 이메일은 변경 불가
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'last_login']
        read_only_fields = ['id', 'date_joined', 'last_login', 'email']
        
    def to_representation(self, instance):
        """응답 데이터 형식 수정"""
        representation = super().to_representation(instance)
        # 프론트엔드에서 사용하는 필드명으로 변환
        representation['name'] = representation.get('first_name', '') + ' ' + representation.get('last_name', '')
        # 한국어 이름 형식도 추가
        representation['bio'] = f"{instance.username}의 블로그입니다."
        return representation
        
    def update(self, instance, validated_data):
        """사용자 정보 업데이트"""
        # 이름 필드가 있는 경우 first_name과 last_name으로 분리
        if 'name' in validated_data:
            name_parts = validated_data.pop('name').split(' ', 1)
            instance.first_name = name_parts[0]
            instance.last_name = name_parts[1] if len(name_parts) > 1 else ''
            
        # 나머지 필드 업데이트
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            
        instance.save()
        return instance

class CategorySerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'author']
        read_only_fields = ['author']
        
    def validate(self, data):
        # 슬러그가 없거나 빈 문자열인 경우 처리
        if 'slug' not in data or not data.get('slug'):
            # 이름에서 슬러그 생성
            if 'name' in data and data['name']:
                import re
                from django.utils.text import slugify
                
                # 기본 슬러그 생성
                slug = slugify(data['name'])
                
                # 영문자가 없는 경우(한글만 있는 경우) 타임스탬프로 슬러그 생성
                if not re.search('[a-zA-Z]', slug):
                    import time
                    slug = f"category-{int(time.time())}"
                
                # 중복 확인
                from .models import Category
                if Category.objects.filter(slug=slug).exists():
                    slug = f"{slug}-{int(time.time())}"
                    
                data['slug'] = slug
            else:
                raise serializers.ValidationError({"name": "카테고리 이름은 필수입니다."})
        
        return data

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'parent', 'content', 'created_at', 'updated_at', 'is_approved', 'replies']
        read_only_fields = ['author', 'is_approved']
    
    def get_replies(self, obj):
        if not hasattr(obj, 'replies'):
            return []
        return CommentSerializer(obj.replies.filter(is_approved=True), many=True).data
        
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category_name = serializers.ReadOnlyField(source='category.name')
    comments = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = '__all__'
        
    def get_comments(self, obj):
        # 최상위 댓글만 반환 (대댓글은 comments.replies에 포함됨)
        comments = obj.comments.filter(parent=None, is_approved=True)
        return CommentSerializer(comments, many=True).data
        
    def validate(self, data):
        # 명시적으로 필수 필드 검증
        if 'title' not in data or not data['title']:
            raise serializers.ValidationError({"title": "제목은 필수 입력 항목입니다."})
            
        if 'content' not in data or not data['content']:
            raise serializers.ValidationError({"content": "내용은 필수 입력 항목입니다."})
            
        if 'category' not in data or not data['category']:
            raise serializers.ValidationError({"category": "카테고리는 필수 선택 항목입니다."})
            
        return data 