from django.shortcuts import render,get_object_or_404
from django.http import Http404, HttpResponseRedirect,HttpResponse
from django.template import  RequestContext,loader
from .models import *
from django_redis import get_redis_connection
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
#from django.db import models
import re
# Create your views here.
def index(request):
    limit = 15
    #universities = University.objects.order_by('id')
    countries = Country.objects.all().order_by("id")
    paginator = Paginator(countries, limit)
    page = request.GET.get('page')  # 获取页码
    try:
        countries = paginator.page(page)  # 获取某页对应的记录
    except PageNotAnInteger:  # 如果页码不是个整数
        countries = paginator.page(1)  # 取第一页的记录
    except EmptyPage:  # 如果页码太大，没有相应的记录
        countries = paginator.page(paginator.num_pages)  # 取最后一页的记
    template = loader.get_template('index.html')
    return render(request, 'index.html', {'countries':countries})  
    #页面重定向：服务器不返回页面，而是告诉浏览器再去请求其他的url。
    # return render(request,'index.html')

def ajax(request):
    for i in request.META:
        print(request.META[i])
    return HttpResponse("okkkkkkkkkkkkkk"+str(request.body)+request.get_host()+request.get_full_path())



def detail(request,university_id):
    user = request.user
    if user.is_authenticated:
        con = get_redis_connection('default')
        history_key = 'history_%d'%user.id
        con.lpush(history_key,university_id)
    return HttpResponse("You're looking at country %s" % (university_id))



