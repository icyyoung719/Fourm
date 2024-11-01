from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
# docs: https://geek-docs.com/django/django-top-articles/1007100_django_creating_views.html
#TODO:用来存放与client交流的函数，可以参考下面的例子，是整个django项目最核心的部分


def hello(request):
   return HttpResponse("world ! ")

def template_run_test(request):
   context = {}
   context['hello'] = 'Hello World!'
   return render(request, 'test_run.html', context)

