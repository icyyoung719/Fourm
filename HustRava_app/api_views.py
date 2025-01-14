import re

from django.http import JsonResponse, Http404
from rest_framework import status
from django.shortcuts import render, get_object_or_404, redirect
from django.core.cache import cache
from .models import User, Post, Comment
from .serializers import UserSerializer, PostSerializer, CommentSerializer
from .util import encrypt, verify, generate_verify_code, send_mail, EMAIL_REGEX

def index(request):
    """ API: Get home page data """
    posts = Post.objects.order_by('-created_at')
    topped_posts = Post.objects.filter(is_topped=True).order_by('-created_at')
    stats = {
        "users": User.objects.count(),
        "posts": Post.objects.count(),
        "comments": Comment.objects.count()
    }
    user = request.session.get("user")
    # serialize
    user_serialized = UserSerializer(user)
    posts_serialized = PostSerializer(posts, many=True)
    topped_posts_serialized = PostSerializer(topped_posts, many=True)

    return JsonResponse({
        "user": user_serialized.data if user_serialized else None,
        "posts": posts_serialized.data,
        "topped_posts": topped_posts_serialized.data,
        "stats": stats
    })

def register(request):
    """ API: Register user """
    if request.method == "POST":
        form_email = request.POST.get('user_email')
        form_password = request.POST.get('password')
        form_verify_code = request.POST.get('verify_code')

        if not form_email or not form_password:
            return JsonResponse({'message': '请填写完整信息'}, status=400)

        if User.objects.filter(email=form_email).exists():
            return JsonResponse({'message': '用户已存在'}, status=400)

        cache_key = f'captcha_{form_email}'
        stored_verify_code = cache.get(cache_key)
        if stored_verify_code and stored_verify_code == form_verify_code:
            cache.delete(cache_key)
            encrypted_password = encrypt(form_password)
            user = User(email=form_email, password=encrypted_password)
            user.save()
            return JsonResponse({'message': '注册成功'})
        else:
            return JsonResponse({'message': '验证码错误'}, status=400)

def send_captcha(request):
    """ API: Send captcha code """
    if request.method == 'POST':
        form_email = request.POST.get('user_email')

        if not form_email:
            return JsonResponse({'message': '请填写邮箱'}, status=400)
        if not re.match(EMAIL_REGEX, form_email):
            return JsonResponse({'message': '邮箱格式不正确'}, status=400)

        captcha = generate_verify_code()
        cache_key = f'captcha_{form_email}'
        cache.set(cache_key, captcha, timeout=300)
        try:
            send_mail(to_addr=form_email, subject='HustRava验证码', body=f'您的验证码为: {captcha}')
            return JsonResponse({'message': '验证码已发送'})
        except Exception as e:
            return JsonResponse({'message': '发送失败'}, status=500)

def login(request):
    """ API: Login user """
    if request.method == "POST":
        form_email = request.POST.get('user_email')
        form_password = request.POST.get('password')
        encrypted_password = encrypt(form_password)

        user = User.objects.filter(email=form_email, password=encrypted_password).first()
        if user:
            request.session['user'] = user.to_dict()
            user_serialized = UserSerializer(user)
            return JsonResponse({'message': '登录成功', 'user': user_serialized.data})
        else:
            return JsonResponse({'message': '用户名或密码错误'}, status=400)

def create(request):
    """ API: Create a post """
    if request.method == "POST":
        if "user" in request.session:
            post_title = request.POST.get('title')
            post_content = request.POST.get('content')
            post_author = get_object_or_404(User, email=request.session["user"]["email"])

            if not post_title or not post_content:
                return JsonResponse({'message': '请填写完整信息'}, status=400)

            post = Post(title=post_title, content=post_content, author=post_author)
            post.save()
            return JsonResponse({'message': '帖子创建成功'})
        else:
            return JsonResponse({'message': '请先登录'}, status=status.HTTP_401_UNAUTHORIZED)

def post_detail(request, post_id):
    """ API: Get post details """
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({'error': '帖子不存在'}, status=404)

    comments = Comment.objects.filter(post=post_id)
    # serialize
    posts_serialized = PostSerializer(post)
    comments_serialized = CommentSerializer(comments,many = True)
    return JsonResponse({
        "post": posts_serialized.data,
        "comments": comments_serialized.data
    })

def comment(request, post_id):
    """ API: Add a comment """
    if request.method == "POST" and "user" in request.session:
        content = request.POST.get('content')
        author = get_object_or_404(User, email=request.session["user"]["email"])
        post = get_object_or_404(Post, id=post_id)

        if content:
            comment = Comment(content=content, author=author, post=post)
            comment.save()
            return JsonResponse({'message': '评论成功'})
        else:
            return JsonResponse({'message': '评论内容不能为空'}, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({'message': '未登录'}, status=status.HTTP_401_UNAUTHORIZED)

def user(request, user_email):
    """ 用户主界面 GET """
    try:
        user = User.objects.get(email=user_email)
    except User.DoesNotExist:
        return JsonResponse({'message': '用户不存在'}, status=status.HTTP_404_NOT_FOUND)

    posts = Post.objects.filter(author=user)
    comments = Comment.objects.filter(author=user)

    user_serialized = UserSerializer(user)
    posts_serialized = PostSerializer(posts, many=True)
    comments_serialized = CommentSerializer(comments, many=True)

    return JsonResponse({
        "target_user": user_serialized.data,
        "posts": posts_serialized.data,
        "comments": comments_serialized.data,
        "user": request.session.get("user", None)
    })

def logout(request):
    """ API: Logout user """
    request.session.flush()
    return JsonResponse({'message': '已退出登录'})

def users(request):
    """ 用户列表 GET """
    user_list = User.objects.order_by('created_at')
    user_serialized = UserSerializer(user_list, many=True)

    return JsonResponse({
        "user_list": user_serialized.data,
        "user": request.session.get("user", None)
    })

def settings(request):
    """ 用户设置 GET """
    if "user" in request.session:
        user_serialized = UserSerializer(request.session["user"])
        return JsonResponse({
            "user": user_serialized.data,
            "status": "success"
        })
    else:
        # 返回 JSON 响应，指示客户端需要重新登录
        return JsonResponse({
            "message": "Please log in.",
            "redirect_url": "/login/",
            "status": "unauthorized"
        }, status=status.HTTP_401_UNAUTHORIZED)
    
def settings_password(request):
    """ 用户设置(密码) GET/POST """
    if request.method == "GET":
        if "user" in request.session:
            user_serialized = UserSerializer(request.session["user"])
            return JsonResponse({
                "user": user_serialized.data
            },status=status.HTTP_200_OK)
        else:
            return JsonResponse({
                "message": "Please log in.",
                "redirect_url": "/login/"
            },status=status.HTTP_401_UNAUTHORIZED)
    elif request.method == "POST":
        form_original_password = request.POST.get('original_password')
        form_new_password = request.POST.get('new_password')
        form_new_password_confirm = request.POST.get('new_password_confirm')
        form_verify_code = request.POST.get('verify_code')

        if "user" in request.session:
            user = get_object_or_404(User, email=request.session["user"]["email"])

            if not verify(form_original_password, user.password):
                return JsonResponse({
                    "message": "原密码错误",
                    "user":  UserSerializer(user).data,
                }, status=400)
            if form_new_password != form_new_password_confirm:
                return JsonResponse({
                    "message": "两次输入的密码不一致",
                    "user": UserSerializer(user).data,
                }, status=400)
            cache_key = f'captcha_{request.session["user"]["email"]}'
            stored_verify_code = cache.get(cache_key)
            if stored_verify_code and stored_verify_code == form_verify_code:
                cache.delete(stored_verify_code)  # 验证成功后删除验证码
            else:
                return JsonResponse({
                    "message": "验证码错误",
                    "user": UserSerializer(user).data,
                }, status=400)

            user.password = encrypt(form_new_password)
            user.save()
            del request.session['user']

        return JsonResponse({
            "message": "密码修改成功",
            "redirect_url": "/login/"
        },status=status.HTTP_200_OK)

def settings_bio(request):
    """ 用户设置(个人简介) GET/POST """
    if request.method == "GET":
        if "user" in request.session:
            user_serialized = UserSerializer(request.session["user"])
            return JsonResponse({
                "user": user_serialized.data
            },status=status.HTTP_200_OK)
        else:
            return JsonResponse({
                "message": "Please log in.",
                "redirect_url": "/login/"
            },status=status.HTTP_401_UNAUTHORIZED)
    elif request.method == "POST":
        form_bio = request.POST.get('bio')
        form_name = request.POST.get('name')

        if "user" in request.session:
            user = get_object_or_404(User, email=request.session["user"]["email"])
            user.bio = form_bio
            user.name = form_name
            user.save()
            user_serialized = UserSerializer(request.session["user"])

            return JsonResponse({
                "user": user_serialized.data
            }, status=status.HTTP_200_OK)

        return JsonResponse({
            "message": "Please log in.",
        }, status=status.HTTP_401_UNAUTHORIZED)
    
def find_password(request):
    """ 找回密码 GET/POST """
    if request.method == "GET":
        if "user" in request.session:
            del request.session['user']
        return JsonResponse({
            "redirect_url": "/find_password/"
        }, status=status.HTTP_200_OK)
    elif request.method == "POST":
        form_email = request.POST.get('user_email')
        form_password = request.POST.get('password')
        form_verify_code = request.POST.get('verify_code')

        if not form_email or not form_password:
            return JsonResponse({'message': '请填写完整信息'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=form_email).first()

        if not user:
            return JsonResponse({'message': '用户不存在，请输入正确的邮箱'}, status=status.HTTP_400_BAD_REQUEST)

        # 验证码是否正确
        cache_key = f'captcha_{form_email}'
        stored_verify_code = cache.get(cache_key)
        if stored_verify_code and stored_verify_code == form_verify_code:
            cache.delete(stored_verify_code)  # 验证成功后删除验证码
        else:
            return JsonResponse({'message': '验证码错误'}, status=status.HTTP_400_BAD_REQUEST)

        encrypted_password = encrypt(form_password)
        user.password = encrypted_password
        user.save()
        return JsonResponse({'message': '密码找回成功'}, status=status.HTTP_200_OK)