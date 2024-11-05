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
    path('admin/', admin.site.urls), # Admin page

    path('', views.index, name = 'index'),  # Homepage view
    path('register/', views.register, name = "register")
    #path('posts/', views.post_list, name = 'post_list'),  # List of posts
    #path('post/<int:id>/', views.post_detail, name = 'post_detail'),  # Post detail
    #path('post/new/', views.create_post, name = 'create_post'),  # Form to create a post

]

