from django.shortcuts import render,get_object_or_404
from django.http import Http404, HttpResponseRedirect,HttpResponse,JsonResponse
from django.template import  RequestContext,loader
import re
from django_redis import get_redis_connection
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.core.cache import cache
from rest_framework.viewsets import ModelViewSet
from universitylist.serializers import *
#from django.db import models
from .models import *

# Create your views here.
class Api(ModelViewSet):
    # queryset是一个查询数据的查询集，存储这所有的数据库查询之后的数据
    queryset = Continent.objects.all()
    serializer_class = UserInfoSerializer
    # serializer_class用来指定在当前的视图里面进行　序列化与反序列时使用的序列化器（串行器）

class Bpi(ModelViewSet):
    # queryset是一个查询数据的查询集，存储这所有的数据库查询之后的数据
    queryset = Country.objects.all()
    serializer_class = UserInfoSerializer
    # serializer_class用来指定在当前的视图里面进行　序列化与反序列时使用的序列化器（串行器）

def index(request):
    """
    context = cache.get('index_page_data')
    if  context is None:
        #universities = University.objects.order_by('id')
        countries = Country.objects.all().order_by("-update_time")
        context={'countries_cache':countries,}
        cache.set('index_page_data',context[countries_cache], 3600)
    """
    limit = 15
    #universities = University.objects.order_by('id')
    countries = Country.objects.all().order_by('-update_time','id')
    paginator = Paginator(countries, limit)
    page = request.GET.get('page')  # 获取页码
    try:
        countries = paginator.page(page)  # 获取某页对应的记录
    except PageNotAnInteger:  # 如果页码不是个整数
        countries = paginator.page(1)  # 取第一页的记录
    except EmptyPage:  # 如果页码太大，没有相应的记录
        countries = paginator.page(paginator.num_pages)  # 取最后一页的记
    template = loader.get_template('index.html')
    #context.update(countries=countries)
    context={'countries':countries}
    return render(request, 'index.html', context)  
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



