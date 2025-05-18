from rest_framework import serializers
from .models import Category, Post, Comment
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

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