from hashlib import sha1

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Post, Comment, Tag, Notification, Bookmark, Follow
from .forms import PostForm, CommentForm  # Make sure to create forms for posts and comments
from django.contrib import messages
from django.utils import timezone

# Create your views here.
# docs: https://geek-docs.com/django/django-top-articles/1007100_django_creating_views.html
# TODO:用来存放与client交流的函数，

# Home view
def index(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'posts': posts})


def register(request):
    """ 注册 GET/POST """
    if request.method == "GET":
        if "logged_in_user" in request.session:
            del request.session['logged_in_user']
        return render(request, 'register.html')
    elif request.method == "POST":
        form_username = request.POST.get('username')
        form_password = request.POST.get('password')

        if form_username == "" or form_password == "":
            return render(request, 'forum_app/register.html', {'error': '请填写完整信息'})

        if len(User.objects.filter(user_name = form_username)) != 0:
            return render(request, 'forum_app/register.html', {'error': '用户已存在'})

        user = User(name = form_username, password = form_password)
        user.save()
        return redirect('/login/')

# Post Detail view
def post_detail(request, post_id):
    post = get_object_or_404(Post, pk = post_id)
    comments = post.comments.all()

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit = False)
            comment.author = request.user
            comment.post = post
            comment.save()
            messages.success(request, "Comment added successfully!")
            return redirect('post_detail', post_id = post.id)
    else:
        form = CommentForm()

    return render(request, 'post_detail.html', {'post': post, 'comments': comments, 'form': form})

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'post_list.html', {'posts': posts})

# Create a new post
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit = False)
            post.author = request.user
            post.created_at = timezone.now()
            post.save()
            messages.success(request, "Post created successfully!")
            return redirect('home')
    else:
        form = PostForm()

    return render(request, 'create_post.html', {'form': form})


# User profile view
def profile(request, user_id):
    user = get_object_or_404(User, pk = user_id)
    posts = user.posts.all()
    followers = user.followers.all()
    following = user.followings.all()
    return render(request, 'profile.html',
                  {'user': user, 'posts': posts, 'followers': followers, 'following': following})


# Follow/unfollow a user
@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, pk = user_id)
    if request.user in user_to_follow.followers.all():
        user_to_follow.followers.remove(request.user)
        messages.info(request, f"You unfollowed {user_to_follow.name}")
    else:
        user_to_follow.followers.add(request.user)
        messages.success(request, f"You followed {user_to_follow.name}")

    return redirect('profile', user_id = user_to_follow.id)


# Bookmark a post
@login_required
def bookmark_post(request, post_id):
    post = get_object_or_404(Post, pk = post_id)
    bookmark, created = Bookmark.objects.get_or_create(user = request.user, post = post)
    if not created:
        bookmark.delete()
        messages.info(request, "Bookmark removed.")
    else:
        messages.success(request, "Post bookmarked.")

    return redirect('post_detail', post_id = post.id)


# Notifications view
@login_required
def notifications(request):
    notifications = request.user.notifications.all().order_by('-created_at')
    return render(request, 'notifications.html', {'notifications': notifications})


# Mark notifications as read
@login_required
def mark_notifications_as_read(request):
    request.user.notifications.filter(is_read = False).update(is_read = True)
    messages.success(request, "Notifications marked as read.")
    return redirect('notifications')


