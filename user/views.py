from django.shortcuts import render,get_object_or_404,redirect
from django.http import Http404, HttpResponseRedirect,HttpResponse
from django.template import  RequestContext,loader
from django.urls import reverse
from django.views.generic import View
import re
from .models import User
# Create your views here.


def register(request):
    if(request.method=='GET'):
        return render(request, 'register.html') 
    else:
        username=request.POST.get('username')
        password=request.POST.get('password')
        password2=request.POST.get('password2')
        email=request.POST.get('email')
        allow = request.POST.get('allow')
        #if not all([username,email,password]):
        #    return render(request,'register.html',{'errmsg':"数据不完整！"})
        #if password != password2:
        #    return render(request,'register.html',{'errmsg':"两次密码不相同"})
        #if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$',email):
        #    return render(request,'register.html',{'errmsg':"邮箱不合法"})
        #if allow != 'on':
        #    return render(request,'register.html',{'errmsg':"请同意协议"})
        try:
            user=User.objects.get(name=username)
        except User.DoesNotExist:
            user=None
        if user:
            return render(request,'register.html',{'errmsg':"用户名已经存在"})
        user=User()
        user.name=username
        user.email=email
        user.password=password
        user.save()
        #return HttpResponse("register successful")
        return redirect(reverse('universitylist:index'))

def detail(request, question_id):
    return HttpResponse("You're looking at university")



class RegisterView(View):
    '''注册'''
    def get(self, request):
        '''显示注册页面'''
        return render(request, 'register.html') 

    def post(self, request):
        username=request.POST.get('username')
        password=request.POST.get('password')
        password2=request.POST.get('password2')
        email=request.POST.get('email')
        allow = request.POST.get('allow')
        #if not all([username,email,password]):
        #    return render(request,'register.html',{'errmsg':"数据不完整！"})
        #if password != password2:
        #    return render(request,'register.html',{'errmsg':"两次密码不相同"})
        #if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$',email):
        #    return render(request,'register.html',{'errmsg':"邮箱不合法"})
        #if allow != 'on':
        #    return render(request,'register.html',{'errmsg':"请同意协议"})
        try:
            user=User.objects.get(name=username)
        except User.DoesNotExist:
            user=None
        if user:
            return render(request,'register.html',{'errmsg':"用户名已经存在"})
        user=User()
        user.name=username
        user.email=email
        user.password=password
        user.save()
        #return HttpResponse("register successful")
        return redirect(reverse('universitylist:index'))