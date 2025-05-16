from rest_framework import serializers
from .models import Category, Post
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category_name = serializers.ReadOnlyField(source='category.name')
    
    class Meta:
        model = Post
        fields = '__all__' 