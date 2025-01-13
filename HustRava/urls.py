"""
URL configuration for HustRava project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from HustRava_app import views

from rest_framework.routers import DefaultRouter  # 确保导入 DefaultRouter
from HustRava_app import api_views

# 创建路由器实例并注册视图集
router = DefaultRouter()

admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),                                            # 管理界面

    path('', views.index, name="index"),                                        # 首页 GET
    path('login/', views.login, name="login"),                                  # 登录 GET/POST
    path('register/', views.register, name="register"),                         # 注册 GET/POST
    path('send_captcha/', views.send_captcha, name = "send_captcha"),  # 发送验证码 POST
    path('create/', views.create, name="create"),                               # 创建帖子 GET/POST
    path('post/<int:post_id>/', views.post, name="post"),                   # 帖子 GET
    path('post/<int:post_id>/comment/', views.comment, name="comment"),             # 回复 POST
    path('user/<str:user_email>/', views.user, name="user"),                     # 用户 GET
    path('logout/', views.logout, name="logout"),                               # 退出登录 GET
    path('users/', views.users, name="users"),                                  # 用户列表 GET
    path('find_password/', views.find_password, name="find_password"),             # 找回密码 GET/POST

    path('settings/', views.settings, name="settings"),                         # 用户设置 GET
    path(
        'settings/password/',
        views.settings_password,
        name="settings_password"
    ),                                                                          # 用户设置(密码) GET/POST
    path('settings/bio/', views.settings_bio, name="settings_bio"),             # 用户设置(个人简介) GET/POST
    path('route/', views.route, name='route'),  # 为 route.html 添加路径

    # API URL配置
    path('api/index/', api_views.index, name='index'),                            # 示例API视图
    path('api/login/', api_views.login, name='login'),                            # 示例API视图集
    path('api/register/', api_views.register, name='register'),                        # 示例API视图集
    path('api/send_captcha/', api_views.send_captcha, name='send_captcha'),  # 示例API视图
    path('api/create/', api_views.create, name='create'),                            # 示例API视图集
    path('api/post/<int:post_id>/', api_views.post_detail, name='post_detail'),  # 示例API视图
    path('api/post/<int:post_id>/comment/', api_views.comment, name='comment'),  # 示例API视图集
    path('api/user/<str:user_email>/', api_views.user, name='user'),                     # 示例API视图集
    path('api/logout/', api_views.logout, name='logout'),                           # 示例API视图集
    path('api/users/', api_views.users, name='users'),                     # 示例API视图
    path('api/find_password/', api_views.find_password, name='find_password'),  # 示例API视图集
    path('api/settings/', api_views.settings, name='settings'),                         # 示例API视图集
    path('api/settings/password/', api_views.settings_password, name='settings_password'),  # 示例API视图集
    path('api/settings/bio/', api_views.settings_bio, name='settings_bio'),  # 示例API视图集
    # path('api/route/', api_views.route, name='route'),  # 为 route.html 添加路径

    path('api/', include(router.urls)),                                        # 包含由路由器生成的URL
]

