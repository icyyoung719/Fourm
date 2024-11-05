from django.contrib import admin

from HustRava_app.models import User, Post, Comment, Tag, Notification

# 为了让 admin 界面管理某个数据模型，我们需要先注册该数据模型到 admin。
# 在 admin 界面中，我们可以对数据模型进行增删改查等操作。
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Notification)
