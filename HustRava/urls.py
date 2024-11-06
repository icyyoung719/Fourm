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
from django.urls import path

from HustRava_app import views

#TODO:需要在此py文件中添加网页子页的url导航
#如：    path('login/', views.login, name="login"),                                  # 登录 GET/POST
#       path('register/', views.register, name="register"),                          # 注册 GET/POST

admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),                                            # 管理界面

    path('', views.index, name="index"),                                        # 首页 GET
    path('login/', views.login, name="login"),                                  # 登录 GET/POST
    path('register/', views.register, name="register"),                         # 注册 GET/POST
    path('create/', views.create, name="create"),                               # 创建帖子 GET/POST
    path('post/<int:topic_id>/', views.post, name="post"),                   # 帖子 GET
    path('post/<int:topic_id>/reply/', views.comment, name="comment"),             # 回复 POST
    path('user/<str:user_name>/', views.user, name="user"),                     # 用户 GET
    path('logout/', views.logout, name="logout"),                               # 退出登录 GET
    path('users/', views.users, name="users"),                                  # 用户列表 GET

    path('settings/', views.settings, name="settings"),                         # 用户设置 GET
    path(
        'settings/password/',
        views.settings_password,
        name="settings_password"
    ),                                                                          # 用户设置(密码) GET/POST
    path('settings/bio/', views.settings_bio, name="settings_bio"),             # 用户设置(个人简介) GET/POST

]

