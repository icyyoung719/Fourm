from django.db import models

# Create your models here.
#TODO: 存放创建的类，如帖子类、用户类、回复类、
# 用户类
class User(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    sex = models.BooleanField(default=True) #  性别字段，True为男，False为女
    age = models.IntegerField(default=0) # 年龄字段
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.jpg') # 头像字段
    posts = models.ManyToManyField('Post', related_name = "users")

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey('User', on_delete = models.CASCADE, related_name = "posts")
    like_nums = models.IntegerField(default = 0)
    # comments =

# 回复类
class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('User', on_delete = models.CASCADE, related_name = "comments")
    post = models.ForeignKey('Post', on_delete = models.CASCADE, related_name = "comments")
    like_nums = models.IntegerField(default = 0)
    sub_comments = models.ManyToManyField('self', related_name = "sub_comments")

# Tag
class Tag(models.Model):
    name = models.CharField(max_length=30)
    posts = models.ManyToManyField('Post', related_name = "tags")

# Notification:For tracking actions and notifying users about updates.
class Notification(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('User', on_delete = models.CASCADE, related_name = "notifications")
    is_read = models.BooleanField(default=False)

# User_profile:For storing additional information about users.
class User_profile(models.Model):
    user = models.OneToOneField('User', on_delete = models.CASCADE, related_name = "profile")
    bio = models.TextField(blank = True) # 个人简介

# Bookmark:Allows users to save posts they want to revisit.
class Bookmark(models.Model):
    user = models.ForeignKey('User', on_delete = models.CASCADE, related_name = "bookmarks")
    post = models.ForeignKey('Post', on_delete = models.CASCADE, related_name = "bookmarks")
    created_at = models.DateTimeField(auto_now_add=True)

# Follow:Allows users to follow each other.
class Follow(models.Model):
    user = models.ForeignKey('User', on_delete = models.CASCADE, related_name = "followings")
    following = models.ForeignKey('User', on_delete = models.CASCADE, related_name = "followers")

