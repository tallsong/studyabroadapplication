from django.shortcuts import render,get_object_or_404,redirect
from django.http import Http404, HttpResponseRedirect,HttpResponse,JsonResponse
from django.template import  RequestContext,loader
import re
from django_redis import get_redis_connection
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.core.cache import cache
from django.urls import reverse
from rest_framework.viewsets import ModelViewSet
from universitylist.serializers import *
from django.db import transaction
from universitylist.models import *
from django.views.decorators.cache import cache_page
from django.views.generic import View
from django.core.cache import cache    # cache.set(key,value,time) cache.get(key)  con=get_redis_connection('default')
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
#@cache_page(60*15)
def index(request):
    """
    context = cache.get('index_page_data')
    if  context is None:
        #universities = University.objects.order_by('id')
        countries = Country.objects.all().order_by("-update_time")
        context={'countries_cache':countries,}
        cache.set('index_page_data',context[countries_cache], 3600)
    """
    limit = 12
    #universities = University.objects.order_by('id')
    universities = University.objects.all().order_by('latest_rank','id')
    paginator = Paginator(universities, limit)
    page = request.GET.get('page')  # 获取页码

    try:
        universities = paginator.page(page)  # 获取某页对应的记录
    except PageNotAnInteger:  # 如果页码不是个整数
        universities = paginator.page(1)  # 取第一页的记录
    except EmptyPage:  # 如果页码太大，没有相应的记录
        universities = paginator.page(paginator.num_pages)  # 取最后一页的记
    num_pages = paginator.num_pages
    try:
        page = int(page)
    except Exception as e:
        page = 1
    if page > paginator.num_pages:   #  num_pages 页面总数
        page = 1
    if num_pages < 5:
        pages = range(1, num_pages+1)
    elif page <= 3:
        pages = range(1, 6)
    elif num_pages - page <= 2:
        pages = range(num_pages-4, num_pages+1)
    else:
        pages = range(page-2, page+3)
    template = loader.get_template('index.html')
    #context.update(countries=countries)
    context={'universities':universities,
             'pages':pages}
    return render(request, 'index.html', context)  
    #页面重定向：服务器不返回页面，而是告诉浏览器再去请求其他的url。
    # return render(request,'index.html')

def ajax(request):
    for i in request.META:
        print(request.META[i])
    return HttpResponse("okkkkkkkkkkkkkk"+str(request.body)+request.get_host()+request.get_full_path())


#@transaction.atomic
def detail(request,university_id):
    user = request.user
    try:
        university = University.objects.get(id=university_id)
    except University.DoesNotExist:
        return redirect(reverse('universitylist:index'))
    is_collect = False
    if user.is_authenticated:
        con = get_redis_connection('default')
        history_key = 'history_%d'%user.id
        university_ids = con.lrange(history_key, 0, 4)
        if(str(university_id).encode() in university_ids):
            con.lrem(history_key,0,university_id)
        con.lpush(history_key,university_id)
    #university = University.object
        collec_key='collect_%s' % user.id
        if(str(university.id).encode() in con.lrange(collec_key,0,-1)):
           is_collect = True
    context={'university':university,'is_collect':is_collect}
    return render(request, 'university_detail.html', context)  



