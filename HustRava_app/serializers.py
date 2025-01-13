from rest_framework import serializers
from .models import User, Post, Comment, Tag, Notification, User_profile, Bookmark, Follow

# Used to serialize models into JSON format
# from models.py

from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password' , 'created_at', 'bio']
        # 如果你想包括所有字段，可以使用 '__all__'
        # fields = '__all__'
        read_only_fields = ['created_at']  # 根据需要设置只读字段

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_at', 'author', 'like_nums', 'is_topped']
        read_only_fields = ['created_at', 'author']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at', 'author', 'post', 'like_nums']
        read_only_fields = ['created_at', 'author', 'post']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'content', 'created_at', 'user', 'is_read']
        read_only_fields = ['created_at', 'user']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_profile
        fields = ['id', 'user', 'bio']
        read_only_fields = ['user']

class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ['id', 'user', 'post', 'created_at']
        read_only_fields = ['created_at']

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['id', 'user', 'following']
