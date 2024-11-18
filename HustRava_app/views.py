import re

from django.http import JsonResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.core.cache import cache
from .models import User, Post, Comment, Tag, Notification, Bookmark, Follow
from .util import encrypt, verify, generate_verify_code, send_mail, EMAIL_REGEX


# Home view
def index(request):
    """ 首页 GET """
    # 将所有帖子按时间排序
    posts = Post.objects.order_by('-created_at')
    if "user" in request.session:
        return render(request, 'index.html', {
            "posts": posts,
            "topped_posts": Post.objects.filter(is_topped=True).order_by('-created_at'),
            "stats": {
                "users": User.objects.count(),
                "posts": Post.objects.count(),
                "comments": Comment.objects.count()
            },
            "user":request.session["user"]
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
        if "user" in request.session:
            del request.session['user']
        return render(request, 'register.html')
    elif request.method == "POST":
        form_email = request.POST.get('user_email')
        form_password = request.POST.get('password')
        form_verify_code = request.POST.get('verify_code')

        if form_email == "" or form_password == "":
            return render(request, 'register.html', {'error': '请填写完整信息'})

        if len(User.objects.filter(email = form_email)) != 0:
            return render(request, 'register.html', {'error': '用户已存在'})

        # 验证码是否正确
        cache_key = f'captcha_{form_email}'
        stored_verify_code = cache.get(cache_key)
        if stored_verify_code and stored_verify_code == form_verify_code:
            cache.delete(stored_verify_code)  # 验证成功后删除验证码
        else:
            return render(request, 'register.html', {'error': '验证码错误'})

        encrypted_password = encrypt(form_password)
        user = User(email = form_email, password = encrypted_password)
        user.save()
        return redirect('/login/')

def send_captcha(request):
    print("call")
    if request.method == 'POST':
        form_email = request.POST.get('user_email')

        if not form_email:
            return JsonResponse({'message': '请填写邮箱'}, status=200)
        if not re.match(EMAIL_REGEX, form_email):
            return JsonResponse({'message': '邮箱格式不正确'}, status=200)

        captcha = generate_verify_code()
        cache_key = f'captcha_{form_email}'
        cache.set(cache_key, captcha, timeout=300)  # 验证码有效期5分钟
        try:
            send_mail(to_addr=form_email, subject='HustRava验证码', body='您的验证码为: ' + captcha)
        except Exception as e:
            return JsonResponse({'error': '发送失败'}, status=500)
        return JsonResponse({'message': '验证码已发送'}, status=200)
    else:
        return JsonResponse({'message': '无效请求'}, status=400)

def login(request):
    """ 登录 GET/POST """
    if request.method == "GET":
        # 如果已经登录, 就退出登录 (手动滑稽)
        if "user" in request.session:
            del request.session['user']
        return render(request, 'login.html')
    elif request.method == "POST":
        form_email = request.POST.get('user_email')
        form_password = request.POST.get('password')
        encrypted_password = encrypt(form_password)

        user = User.objects.filter(email=form_email, password=encrypted_password).first()
        if user:
            request.session['user'] = user.to_dict()
            return redirect('/')
        else:
            return render(request, 'login.html', {'error': '用户名或密码错误'})

def create(request):
    """ 创建帖子 GET/POST """
    if request.method == "GET":
        if "user" in request.session:
            return render(request, 'create.html', {
                "user": request.session["user"]
            })
        else:
            return redirect('/login/')
    elif request.method == "POST":
        if "user" in request.session:
            post_title = request.POST.get('title')
            post_content = request.POST.get('content')
            user_data = request.session["user"]
            post_author = get_object_or_404(User, email = request.session["user"]["email"])

            if post_title == "" or post_content == "":
                return render(request, 'create.html', {
                    "error": "请填写完整信息",
                    "logged_in_user": request.session["logged_in_user"]
                })

            post = Post(title=post_title, content=post_content, author=post_author)
            post.save()
        else:
            return redirect('/login/')
        return redirect('/')


def post(request, post_id):
    """ 帖子 GET """
    try:
        post = Post.objects.get(id = post_id)
    except:
        raise Http404("帖子不存在")

    if "user" in request.session:
        return render(request, 'post.html', {
            "post": post,
            "comments": Comment.objects.filter(post = post_id),
            "user": request.session["user"]
        })
    else:
        return render(request, 'post.html', {
            "post": post,
            "comments": Comment.objects.filter(post = post_id)
        })

def comment(request, post_id):
    """ 回复 POST """
    if request.method == "POST":
        if "user" in request.session:
            comment_content = request.POST.get('content')
            comment_author = get_object_or_404(User, email = request.session["user"]["email"])
            comment_post = Post.objects.filter(id=post_id).first()

            if comment_content != "":
                comment = Comment(content=comment_content, author=comment_author, post=comment_post)
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

    if "user" in request.session:
        return render(request, 'user.html', {
            'target_user': user,
            'posts': Post.objects.filter(author=user),
            'comments': Comment.objects.filter(author=user),
            'user': request.session["user"]
        })
    else:
        return render(request, 'user.html', {
            'target_user': user,
            'posts': Post.objects.filter(author=user),
            'comments': Comment.objects.filter(author=user),
        })

def logout(request):
    """ 退出登录 GET """
    try:
        del request.session['user']
    except KeyError:
        pass
    return redirect('/')

def users(request):
    """ 用户列表 GET """
    user_list = User.objects.order_by('created_at')
    if "user" in request.session:
        return render(request, 'users.html', {
            "user_list": user_list,
            "user": request.session["user"]
        })
    else:
        return render(request, 'users.html', {"user_list": user_list})

def settings(request):
    """ 用户设置 GET """
    if "user" in request.session:
        return render(request, 'settings.html', {
            "user": request.session["user"]
        })
    else:
        return redirect('/login/')

def settings_password(request):
    """ 用户设置(密码) GET/POST """
    if request.method == "GET":
        if "user" in request.session:
            return render(request, 'settings_password.html', {
                "user": request.session["user"],
            })
        else:
            return redirect('/login/')
    elif request.method == "POST":
        form_original_password = request.POST.get('original_password')
        form_new_password = request.POST.get('new_password')
        form_new_password_confirm = request.POST.get('new_password_confirm')
        form_verify_code = request.POST.get('verify_code')

        if "user" in request.session:
            user = get_object_or_404(User, email = request.session["user"]["email"])

            if not verify(form_original_password, user.password):
                return render(request, 'settings_password.html', {
                    "error": "原密码错误",
                    "user": request.session["user"],
                    "user_obj": user
                })
            if form_new_password != form_new_password_confirm:
                return render(request, 'settings_password.html', {
                    "error": "两次输入的密码不一致",
                    "user": request.session["user"],
                })
            cache_key = f'captcha_'+request.session["logged_in_user_email"]
            stored_verify_code = cache.get(cache_key)
            if stored_verify_code and stored_verify_code == form_verify_code:
                cache.delete(stored_verify_code)  # 验证成功后删除验证码
            else:
                return render(request, 'settings_password.html', {
                    "error": "验证码错误",
                    "user": request.session["user"],
                })

            user.password = encrypt(form_new_password)
            user.save()
            del request.session['user']

        return redirect('/login/')

def settings_bio(request):
    """ 用户设置(个人简介) GET/POST """
    if request.method == "GET":
        if "user" in request.session:
            return render(request, 'settings_bio.html', {
                "user": request.session["user"]
            })
        else:
            return redirect('/login/')
    elif request.method == "POST":
        form_bio = request.POST.get('bio')
        form_name = request.POST.get('name')

        if "user" in request.session:
            user = get_object_or_404(User, email = request.session["user"]["email"])
            user.bio = form_bio
            user.name = form_name
            user.save()
            request.session['user'] = user.to_dict()

            return render(request, 'settings_bio.html', {
                "user": user.to_dict(),
            })

        return redirect('/settings/bio/')

def find_password(request):
    """ 找回密码 GET/POST """
    if request.method == "GET":
        if "user" in request.session:
            del request.session['user']
        return render(request, 'find_password.html')
    elif request.method == "POST":
        form_email = request.POST.get('user_email')
        form_password = request.POST.get('password')
        form_verify_code = request.POST.get('verify_code')

        if form_email == "" or form_password == "":
            return render(request, 'find_password.html', {'error': '请填写完整信息'})

        user = User.objects.filter(email = form_email).first()

        if not user:
            return render(request, 'find_password.html', {'error': '用户不存在，请输入正确的邮箱'})

        # 验证码是否正确
        cache_key = f'captcha_{form_email}'
        stored_verify_code = cache.get(cache_key)
        if stored_verify_code and stored_verify_code == form_verify_code:
            cache.delete(stored_verify_code)  # 验证成功后删除验证码
        else:
            return render(request, 'find_password.html', {'error': '验证码错误'})

        encrypted_password = encrypt(form_password)
        user.password = encrypted_password
        user.save()
        return redirect('/login/')


def route(request):
    if request.method == "GET":
        return render(request, 'route.html')
