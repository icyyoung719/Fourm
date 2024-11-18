import string
import random

from django.db import models

# Create your models here.
#TODO: 存放创建的类，如帖子类、用户类、回复类、
# 用户类
class User(models.Model):
    # is_staff = models.BooleanField(default=False)#是否有管理员权限
    name = models.CharField(max_length=30,blank=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    bio = models.TextField(max_length = 100, blank=True)
    def save(self, *args, **kwargs):
        # Set default name if name is empty
        if not self.name:
            self.name = f"User_{self.email}"
        super().save(*args, **kwargs)
    # convert to dict, to pass a user object to the front end
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "created_at": self.created_at.isoformat(),
            "bio": self.bio,
        }
    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey('User', on_delete = models.CASCADE, related_name = "posts")
    like_nums = models.IntegerField(default = 0)
    is_topped = models.BooleanField("置顶帖子", default=False)

    def __str__(self):
        return self.title

# 回复类
class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('User', on_delete = models.CASCADE, related_name = "comments")
    post = models.ForeignKey('Post', on_delete = models.CASCADE, related_name = "comments")
    like_nums = models.IntegerField(default = 0)
    # sub_comments = models.ManyToManyField('self', related_name = "sub_comments")

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

