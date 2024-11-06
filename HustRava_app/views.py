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
    """ 首页 GET """
    # 将所有帖子按时间排序
    posts = Post.objects.order_by('-created_at')
    if "logged_in_user" in request.session:
        return render(request, 'index.html', {
            "topics": posts,
            "topped_topics": Post.objects.filter(is_topped=True).order_by('-created_at'),
            "stats": {
                "users": User.objects.count(),
                "topics": Post.objects.count(),
                "replies": Comment.objects.count()
            },
            "logged_in_user": request.session["logged_in_user"]
        })
    else:
        return render(request, 'index.html', {
            "topics": posts,
            "stats": {
                "users": User.objects.count(),
                "topics": Post.objects.count(),
                "replies": Comment.objects.count()
            },
            "topped_topics": Post.objects.filter(is_topped=True).order_by('-created_at')
        })

def register(request):
    """ 注册 GET/POST """
    if request.method == "GET":
        if "logged_in_user" in request.session:
            del request.session['logged_in_user']
        return render(request, 'register.html')
    elif request.method == "POST":
        form_email = request.POST.get('email')
        form_password = request.POST.get('password')

        if form_email == "" or form_password == "":
            return render(request, 'register.html', {'error': '请填写完整信息'})

        if len(User.objects.filter(email = form_email)) != 0:
            return render(request, 'register.html', {'error': '用户已存在'})

        user = User(email = form_email, password = form_password)
        user.save()
        return redirect('/login/')

def login(request):
    """ 登录 GET/POST """
    if request.method == "GET":
        # 如果已经登录, 就退出登录 (手动滑稽)
        if "logged_in_user" in request.session:
            del request.session['logged_in_user']
        return render(request, 'login.html')
    elif request.method == "POST":
        form_email = request.POST.get('email')
        form_password = request.POST.get('password')

        user = User.objects.filter(email=form_email, password=form_password).first()
        if user:
            # 弹窗提示登录
            print("登陆成功")
            messages.success(request, "登录成功")
            request.session['logged_in_user'] = user.name
            return redirect('register')
        else:
            return render(request, 'login.html', {'error': '用户名或密码错误'})

def create(request):
    """ 创建帖子 GET/POST """
    if request.method == "GET":
        if "logged_in_user" in request.session:
            return render(request, 'create.html', {
                "logged_in_user": request.session["logged_in_user"]
            })
        else:
            return redirect('/login/')
    elif request.method == "POST":
        if "logged_in_user" in request.session:
            form_title = request.POST.get('title')
            form_content = request.POST.get('content')
            form_author = User.objects.filter(name=request.session["logged_in_user"]).first()

            if form_title == "" or form_content == "":
                return render(request, 'create.html', {
                    "error": "请填写完整信息",
                    "logged_in_user": request.session["logged_in_user"]
                })

            post = Post(itle=form_title, content=form_content, author=form_author)
            post.save()
        else:
            return redirect('/login/')
        return redirect('/')


def post(request, post_id):
    """ 帖子 GET """
    try:
        post = Post.objects.get(id = post_id)
    except:
        raise Http404("帖子pos不存在")

    if "logged_in_user" in request.session:
        return render(request, 'post.html', {
            "topic": post,
            "replies": Comment.objects.filter(post = post_id),
            "logged_in_user": request.session["logged_in_user"]
        })
    else:
        return render(request, 'post.html', {
            "topic": post,
            "replies": Comment.objects.filter(post = post_id)
        })

def comment(request, post_id):
    """ 回复 POST """
    if request.method == "POST":
        if "logged_in_user" in request.session:
            form_content = request.POST.get('content')
            form_author = User.objects.filter(name=request.session["logged_in_user"]).first()
            form_post = Post.objects.filter(id=post_id).first()

            if form_content != "":
                reply = Comment(content=form_content, author=form_author, post=form_post)
                reply.save()
            return redirect('/post/{}/'.format(post_id))
        else:
            return redirect('/login/')


def user(request, user_email):
    """ 用户 GET """
    users = list(User.objects.filter(email=user_email))
    if len(users) == 0:
        raise Http404("用户不存在")
    user_obj = users[0]
    if "logged_in_user" in request.session:
        return render(request, 'user.html', {
            'user': user_obj,
            'topics': Post.objects.filter(author=user_obj),
            'replies': Comment.objects.filter(author=user_obj),
            'logged_in_user': request.session["logged_in_user"]
        })
    else:
        return render(request, 'user.html', {
            'user': user_obj,
            'topics': Post.objects.filter(author=user_obj),
            'replies': Comment.objects.filter(author=user_obj),
        })

def logout(request):
    """ 退出登录 GET """
    try:
        del request.session['logged_in_user']
    except KeyError:
        pass
    return redirect('/')

def users(request):
    """ 用户列表 GET """
    user_list = User.objects.order_by('user_create_date')
    if "logged_in_user" in request.session:
        return render(request, 'users.html', {
            "user_list": user_list,
            "logged_in_user": request.session["logged_in_user"]
        })
    else:
        return render(request, 'users.html', {"user_list": user_list})

def settings(request):
    """ 用户设置 GET """
    if "logged_in_user" in request.session:
        return render(request, 'settings.html', {
            "logged_in_user": request.session["logged_in_user"]
        })
    else:
        return redirect('/login/')

def settings_password(request):
    """ 用户设置(密码) GET/POST """
    if request.method == "GET":
        if "logged_in_user" in request.session:
            return render(request, 'settings_password.html', {
                "logged_in_user": request.session["logged_in_user"],
                "user_obj": User.objects.filter(user_name=request.session["logged_in_user"]).first()
            })
        else:
            return redirect('/login/')
    elif request.method == "POST":
        form_original_password = request.POST.get('original_password')
        form_new_password = request.POST.get('new_password')
        form_new_password_confirm = request.POST.get('new_password_confirm')

        if "logged_in_user" in request.session:
            user = User.objects.filter(user_name=request.session["logged_in_user"]).first()

            if form_original_password != user.password:
                return render(request, 'settings_password.html', {
                    "error": "原密码错误",
                    "logged_in_user": request.session["logged_in_user"],
                    "user_obj": user
                })
            if form_new_password != form_new_password_confirm:
                return render(request, 'settings_password.html', {
                    "error": "两次输入的密码不一致",
                    "logged_in_user": request.session["logged_in_user"],
                    "user_obj": user
                })

            user.password = form_new_password
            user.save()
            del request.session['logged_in_user']

        return redirect('/login/')

def settings_bio(request):
    """ 用户设置(个人简介) GET/POST """
    if request.method == "GET":
        if "logged_in_user" in request.session:
            return render(request, 'settings_bio.html', {
                "logged_in_user": request.session["logged_in_user"],
                "user_obj": User.objects.filter(name=request.session["logged_in_user"]).first()
            })
        else:
            return redirect('/login/')
    elif request.method == "POST":
        form_bio = request.POST.get('bio')

        if "logged_in_user" in request.session:
            user = User.objects.filter(name=request.session["logged_in_user"]).first()
            user.user_bio = form_bio
            user.save()

        return redirect('/settings/bio/')
