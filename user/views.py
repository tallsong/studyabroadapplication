from django.shortcuts import render,get_object_or_404,redirect
from django.http import Http404, HttpResponseRedirect,HttpResponse,JsonResponse
from django.template import  RequestContext,loader
from django.urls import reverse
from django.contrib.auth import authenticate, login,logout
from django.views.generic import View
from django.conf import settings
from django.core.mail import send_mail
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from utils.mixin import LoginRequiredMixin
from django_redis import get_redis_connection
import re
from user.models import User
from universitylist.models import Country,University
from celery_tasks.tasks import send_register_active_email
# Create your views here.




class HistoryView(LoginRequiredMixin,View):
    def get(self, request):
        # 获取用户的个人信息
        user = request.user
        con = get_redis_connection('default')
        history_key = 'history_%d' % user.id
        university_ids = con.lrange(history_key, 0, -1)
        university_list = []
        for id in university_ids:
            university = University.objects.get(id=id)
            university_list.append(university)

        ## 组织上下文
        context = {'university_list':university_list,}

        #除了你给模板文件传递的模板变量之外，django框架会把request.user也传给模板文件
        return render(request, 'history.html', context)
class FavoriteView(LoginRequiredMixin,View):
    '''用户中心-信息页'''
    def get(self, request):
        # 获取用户的个人信息
        user = request.user
        con = get_redis_connection('default')
        history_key = 'collect_%d' % user.id
        university_ids = con.lrange(history_key, 0, -1)
        university_list = []
        for id in university_ids:
            university = University.objects.get(id=int(id))
            university_list.append(university)

        ## 组织上下文
        context = {'university_list':university_list,}

        #除了你给模板文件传递的模板变量之外，django框架会把request.user也传给模板文件
        return render(request, 'collect.html', context)

class LoginView(View):
    def get(self, request):
        '''显示登录页面'''
        # 判断是否记住了用户名
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
            checked = 'checked'
        else:
            username = ''
            checked = ''

        # 使用模板
        return render(request, 'login.html', {'username':username, 'checked':checked})
    def post(self, request):
        '''登录校验'''
        # 接收数据
        username = request.POST.get('username')
        password = request.POST.get('password')

        # 校验数据
        if not all([username, password]):
            return render(request, 'login.html', {'errmsg':'数据不完整'})
        try:
            if not User.objects.get(username=username).is_active:
                return render(request, 'login.html', {'errmsg':'账户未激活,请检查邮件激活账户'})
        except Exception as e:
            #print(e.args)
            pass
        # 业务处理:登录校验
        user = authenticate(username=username, password=password)
      
        if user is not None:
            # 用户名密码正确

            if user.is_active:
                # 用户已激活
                # 记录用户的登录状态
                
                login(request, user)
                
                # 跳转到首页
                response = redirect(reverse('universitylist:index')) # HttpResponseRedirect

                # 判断是否需要记住用户名
                remember = request.POST.get('remember')

                if remember == 'on':
                    # 记住用户名
                    response.set_cookie('username', username, max_age=7 * 24 * 3600)
                else:
                    response.delete_cookie('username')

                # 返回response              
                return response
                
        else:
            # 用户名或密码错误
            return render(request, 'login.html', {'errmsg':'用户名或密码错误'})



    #def get(self, request):
    #    return render(request, 'login.html')
    #def post(self, request):
    #    email=request.POST.get('email')
    #    password=request.POST.get('password')
    #    if not all([email,password]):
    #        return render(request,'login.html',{'errmsg':"请输入用户名和密码"})
    #    try:
    #        user=User.objects.get(email=email,is_active=1)
    #    except User.DoesNotExist:
    #        user=None
    #    if not user:
    #        return render(request,'register.html',{'errmsg':'''邮箱不存在请先<a href="/user/register/"  style="margin-top:8px" id="register-button">注册</a>'''})
    #    if(user.password!=password):
    #        return render(request,'login.html',{'errmsg':"密码错误"})
    #    else:
    #        return render(request,'login.html',{'errmsg':"login successful"})
class LogoutView(View):
    '''退出登录'''
    def get(self, request):
        '''退出登录'''
        # 清除用户的session信息
        logout(request)

        # 跳转到首页
        return redirect(reverse('universitylist:index'))


class RegisterView(View):
    '''注册'''
    def get(self, request):
        '''显示注册页面'''
        return render(request, 'register.html') 

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        allow = request.POST.get('allow')
        if not all([username,email,password]):
            return render(request,'register.html',{'errmsg':"数据不完整！"})
        if password != password2:
            return render(request,'register.html',{'errmsg':"两次密码不相同"})
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$',email):
            return render(request,'register.html',{'errmsg':"邮箱不合法"})
        if allow != 'on':
            return render(request,'register.html',{'errmsg':"请同意协议"})
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None
        if user:
            return render(request,'register.html',{'errmsg':'''用户名已经存在，请直接<a href="/user/login/"  style="margin-top:8px" id="register-button">登录</a>或者更换用户名重新注册'''})
        #user=User()
        #user.username=username
        #user.email=email
        #user.password=password
        user = User.objects.create_user(username, email, password)
        user.is_active = 0
        user.save()

        ser = Serializer(settings.SECRET_KEY,3600)
        info = {'confirm':user.id}
        token = ser.dumps(info)
        token = token.decode() # 默认为utf-8
        send_register_active_email.delay(email,username,token)
        #send_mail(subject, message, sender, receiver,
        #html_message=html_message)
        #send_mail(subject,message,sender,receiver)
        return render(request,'login.html',{'errmsg':'注册邮件已经成功发送到您的邮箱，请点击邮箱激活账号'})
        #return redirect(reverse('universitylist:index'))

class ActiveView(View):
    '''用户激活'''
    def get(self, request, token):
        '''进行用户激活'''
        # 进行解密，获取要激活的用户信息
        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
            info = serializer.loads(token)
            # 获取待激活用户的id
            user_id = info['confirm']

            # 根据id获取用户信息
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()

            # 跳转到登录页面
            return redirect(reverse('user:login'))
        except SignatureExpired as e:
            # 激活链接已过期
            return HttpResponse('<h1>激活链接已过期</h1>')


class UserInfoView(LoginRequiredMixin,View):
    '''用户中心-信息页'''
    def get(self, request):
        # 获取用户的个人信息
        user = request.user
        con = get_redis_connection('default')
        history_key = 'history_%d' % user.id
        university_ids = con.lrange(history_key, 0, 4)
        university_list = []
        for id in university_ids:
            university = University.objects.get(id=int(id))
            university_list.append(university)

        ## 组织上下文
        context = {"country":user.country,"toefl":user.toefl,"degree_type":user.degree_type,"fee":user.fee}

        #除了你给模板文件传递的模板变量之外，django框架会把request.user也传给模板文件
        return render(request, 'user_info.html', context)
    def post(self, request):
        user = request.user
        user.country=request.POST.get('country')
        user.toefl=request.POST.get('toefl')
        user.degree_type=request.POST.get('degree_type')
        user.fee=request.POST.get('fee')
        user.save()
        context = {"country":user.country,"toefl":user.toefl,"degree_type":user.degree_type,"fee":user.fee}
        return render(request, 'user_info.html', context)
class CollectView(View):
    def post(self,request):
        user = request.user
        if not user.is_authenticated:
            # 用户未登录
            return JsonResponse({'res':0, 'msg':'loginfirst'})
        university_id=request.POST.get('university_id')
        collec_key='collect_%s' % user.id
        type=request.POST.get('type')
        if(type=='add'):
            con = get_redis_connection('default')
            con.lpush(collec_key,int(university_id))
            return JsonResponse({'res':1, 'msg':'collect successful'})
        elif(type=="minus"):
            con = get_redis_connection('default')
            con.lrem(collec_key,0,int(university_id))
            return JsonResponse({'res':2, 'msg':'minus successful'})

def register(request):
    if(request.method == 'GET'):
        return render(request, 'register.html') 
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        allow = request.POST.get('allow')
        #if not all([username,email,password]):
        #    return render(request,'register.html',{'errmsg':"数据不完整！"})
        #if password != password2:
        #    return render(request,'register.html',{'errmsg':"两次密码不相同"})
        #if not
        #re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$',email):
        #    return render(request,'register.html',{'errmsg':"邮箱不合法"})
        #if allow != 'on':
        #    return render(request,'register.html',{'errmsg':"请同意协议"})
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None
        if user:
            return render(request,'register.html',{'errmsg':"用户名已经存在"})
        user = User()
        user.username = username
        user.email = email
        user.password = password
        user.save()
        #return HttpResponse("register successful")
        return redirect(reverse('universitylist:index'))

def detail(request, question_id):
    return HttpResponse("You're looking at university")