from django.shortcuts import render,get_object_or_404
from django.http import Http404, HttpResponseRedirect,HttpResponse
from django.template import  RequestContext,loader
from .models import University
import re
# Create your views here.
def index(request):
    universities = University.objects.order_by('id')
    template = loader.get_template('index.html')
    context = {
        'universitylist': "havard",
        'universities':universities,
    }
    
    return render(request, 'index.html', context)  
    #页面重定向：服务器不返回页面，而是告诉浏览器再去请求其他的url。
    # return render(request,'index.html')

def ajax(request):
    for i in request.META:
        print(request.META[i])
    return HttpResponse("okkkkkkkkkkkkkk"+str(request.body)+request.get_host()+request.get_full_path())

def register(request):
    context = {
        'universitylist': "havard",
    }
    
    return render(request, 'register.html', context) 

def register_handle(request):
    username=request.POST.get('username')
    password=request.POST.get('password')
    email=request.POST.get('email')
    allow = request.POST.get('allow')
    #if not all([username,email,password]):
    #    return render(request,'register.html',{'errmsg':"数据不完整！"})
    #if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$',email):
    #    return render(request,'register.html',{'errmsg':"邮箱不合法"})
    #if allow != 'on':
    #    return render(request,'register.html',{'errmsg':"请同意协议"})
    print(username)
    return HttpResponse("register successful")

def detail(request, question_id):
    return HttpResponse("You're looking at university %s." % university_id)



