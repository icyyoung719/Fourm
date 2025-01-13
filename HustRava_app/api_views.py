import re

from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404
from django.core.cache import cache
from .models import User, Post, Comment
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
    return JsonResponse({
        "user": user,
        "posts": [post for post in posts],
        "topped_posts": [post for post in topped_posts],
        "stats": stats
    })

def register(request):
    """ API: Register user """
    if request.method == "POST":
        form_email = request.POST.get('user_email')
        form_password = request.POST.get('password')
        form_verify_code = request.POST.get('verify_code')

        if not form_email or not form_password:
            return JsonResponse({'error': '请填写完整信息'}, status=400)

        if User.objects.filter(email=form_email).exists():
            return JsonResponse({'error': '用户已存在'}, status=400)

        cache_key = f'captcha_{form_email}'
        stored_verify_code = cache.get(cache_key)
        if stored_verify_code and stored_verify_code == form_verify_code:
            cache.delete(cache_key)
            encrypted_password = encrypt(form_password)
            user = User(email=form_email, password=encrypted_password)
            user.save()
            return JsonResponse({'message': '注册成功'})
        else:
            return JsonResponse({'error': '验证码错误'}, status=400)

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
            return JsonResponse({'error': '发送失败'}, status=500)

def login(request):
    """ API: Login user """
    if request.method == "POST":
        form_email = request.POST.get('user_email')
        form_password = request.POST.get('password')
        encrypted_password = encrypt(form_password)

        user = User.objects.filter(email=form_email, password=encrypted_password).first()
        if user:
            request.session['user'] = user.to_dict()
            return JsonResponse({'message': '登录成功', 'user': user.to_dict()})
        else:
            return JsonResponse({'error': '用户名或密码错误'}, status=400)

def create(request):
    """ API: Create a post """
    if request.method == "POST":
        if "user" in request.session:
            post_title = request.POST.get('title')
            post_content = request.POST.get('content')
            post_author = get_object_or_404(User, email=request.session["user"]["email"])

            if not post_title or not post_content:
                return JsonResponse({'error': '请填写完整信息'}, status=400)

            post = Post(title=post_title, content=post_content, author=post_author)
            post.save()
            return JsonResponse({'message': '帖子创建成功'})
        else:
            return JsonResponse({'error': '请先登录'}, status=401)

def post_detail(request, post_id):
    """ API: Get post details """
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({'error': '帖子不存在'}, status=404)

    comments = Comment.objects.filter(post=post_id)
    return JsonResponse({
        "post": post,
        "comments": [comment for comment in comments]
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
            return JsonResponse({'error': '评论内容不能为空'}, status=400)
    return JsonResponse({'error': '未登录'}, status=401)

def logout(request):
    """ API: Logout user """
    request.session.flush()
    return JsonResponse({'message': '已退出登录'})
