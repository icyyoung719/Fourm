from hashlib import sha1

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from .models import User, Post, Comment, Tag, Notification, Bookmark, Follow

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
            "posts": posts,
            "topped_posts": Post.objects.filter(is_topped=True).order_by('-created_at'),
            "stats": {
                "users": User.objects.count(),
                "posts": Post.objects.count(),
                "comments": Comment.objects.count()
            },
            "logged_in_user": request.session["logged_in_user"],
            "logged_in_user_email":request.session["logged_in_user_email"]
        })
    else:
        return render(request, 'index.html', {
            "posts": posts,
            "stats": {
                "users": User.objects.count(),
                "posts": Post.objects.count(),
                "comments": Comment.objects.count()
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
        form_email = request.POST.get('user_email')
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
            del request.session['logged_in_user_email']
        return render(request, 'login.html')
    elif request.method == "POST":
        form_email = request.POST.get('user_email')
        form_password = request.POST.get('password')

        user = User.objects.filter(email=form_email, password=form_password).first()
        if user:
            request.session['logged_in_user'] = user.name
            request.session['logged_in_user_email'] = user.email
            return redirect('/')
        else:
            return render(request, 'login.html', {'error': '用户名或密码错误'})

def create(request):
    """ 创建帖子 GET/POST """
    if request.method == "GET":
        if "logged_in_user" in request.session:
            return render(request, 'create.html', {
                "logged_in_user": request.session["logged_in_user"],
                "logged_in_user_email": request.session["logged_in_user_email"]
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

            post = Post(title=form_title, content=form_content, author=form_author)
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
            "post": post,
            "comments": Comment.objects.filter(post = post_id),
            "logged_in_user": request.session["logged_in_user"],
            "logged_in_user_email": request.session["logged_in_user_email"]
        })
    else:
        return render(request, 'post.html', {
            "post": post,
            "comments": Comment.objects.filter(post = post_id)
        })

def comment(request, post_id):
    """ 回复 POST """
    if request.method == "POST":
        if "logged_in_user" in request.session:
            form_content = request.POST.get('content')
            form_author = User.objects.filter(email=request.session["logged_in_user_email"]).first()
            form_post = Post.objects.filter(id=post_id).first()

            if form_content != "":
                comment = Comment(content=form_content, author=form_author, post=form_post)
                comment.save()
            return redirect('/post/{}/'.format(post_id))
        else:
            return redirect('/login/')


def user(request, user_email):
    """ 用户主界面 GET """
    try:
        user = User.objects.get(email = user_email)
    except:
        raise Http404("用户不存在")

    if "logged_in_user" in request.session:
        return render(request, 'user.html', {
            'user': user,
            'posts': Post.objects.filter(author=user),
            'comments': Comment.objects.filter(author=user),
            'logged_in_user': request.session["logged_in_user"],
            'logged_in_user_email': request.session["logged_in_user_email"]
        })
    else:
        return render(request, 'user.html', {
            'user': user,
            'posts': Post.objects.filter(author=user),
            'comments': Comment.objects.filter(author=user),
        })

def logout(request):
    """ 退出登录 GET """
    try:
        del request.session['logged_in_user']
        del request.session['logged_in_user_email']
    except KeyError:
        pass
    return redirect('/')

def users(request):
    """ 用户列表 GET """
    user_list = User.objects.order_by('created_at')
    if "logged_in_user" in request.session:
        return render(request, 'users.html', {
            "user_list": user_list,
            "logged_in_user": request.session["logged_in_user"],
            "logged_in_user_email": request.session["logged_in_user_email"]
        })
    else:
        return render(request, 'users.html', {"user_list": user_list})

def settings(request):
    """ 用户设置 GET """
    if "logged_in_user" in request.session:
        return render(request, 'settings.html', {
            "logged_in_user": request.session["logged_in_user"],
            "logged_in_user_email": request.session["logged_in_user_email"]
        })
    else:
        return redirect('/login/')

def settings_password(request):
    """ 用户设置(密码) GET/POST """
    if request.method == "GET":
        if "logged_in_user" in request.session:
            return render(request, 'settings_password.html', {
                "logged_in_user": request.session["logged_in_user"],
                "logged_in_user_email": request.session["logged_in_user_email"],
                "user_obj": User.objects.filter(email=request.session["logged_in_user_email"]).first()
            })
        else:
            return redirect('/login/')
    elif request.method == "POST":
        form_original_password = request.POST.get('original_password')
        form_new_password = request.POST.get('new_password')
        form_new_password_confirm = request.POST.get('new_password_confirm')

        if "logged_in_user" in request.session:
            user = User.objects.filter(email=request.session["logged_in_user_email"]).first()

            if form_original_password != user.password:
                return render(request, 'settings_password.html', {
                    "error": "原密码错误",
                    "logged_in_user": request.session["logged_in_user"],
                    "logged_in_user_email": request.session["logged_in_user_email"],
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
            del request.session['logged_in_user_email']

        return redirect('/login/')

def settings_bio(request):
    """ 用户设置(个人简介) GET/POST """
    if request.method == "GET":
        if "logged_in_user" in request.session:
            return render(request, 'settings_bio.html', {
                "logged_in_user": request.session["logged_in_user"],
                "logged_in_user_email": request.session["logged_in_user_email"],
                "user_obj": User.objects.filter(email=request.session["logged_in_user_email"]).first()
            })
        else:
            return redirect('/login/')
    elif request.method == "POST":
        form_bio = request.POST.get('bio')

        if "logged_in_user" in request.session:
            user = User.objects.filter(email=request.session["logged_in_user_email"]).first()
            user.bio = form_bio
            user.save()

        return redirect('/settings/bio/')
