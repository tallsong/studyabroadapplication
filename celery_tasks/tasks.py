# 使用celery
from django.core.mail import send_mail
from django.template import loader, RequestContext
from django.conf import settings
from celery import Celery
import time

#在任务处理者一端加这几句
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studyabroadapplication.settings')
django.setup()
from universitylist.models import *
from django_redis import get_redis_connection
# 创建一个Celery类的实例对象
app = Celery('celery_tasks.tasks', broker='redis://127.0.0.1:6379/8')

# celery -A celery_tasks.tasks worker -l info 任务执行端使用次命令执行函数  windows：   celery -A celery_tasks.tasks worker -l info -P eventlet
# 定义任务函数
@app.task
def send_register_active_email(email, username, token):
    '''发送激活邮件'''
    # 组织邮件信息
    subject = 'welcome to STUDYABROADAPPLICATION'
    message = ''
    sender = settings.EMAIL_FROM
    receiver = [email]
    html_message = '<h1>%s, welocme to join a member of STUDYABROADAPPLICATION</h1>please click the link below to active your account<a href="http://%s/user/active/%s">link</a> <br/> <h1>http://%s/user/active/%s</h1>' % (username,settings.MY_HOST,token,settings.MY_HOST,token)
    send_mail(subject,message,sender,receiver,html_message=html_message)


@app.task
def generate_static_index_html():
    '''产生首页静态页面'''
    countries = Country.objects.all().order_by("-update_time")
    # 组织模板上下文
    context = {'countries':countries}
    # 使用模板
    # 1.加载模板文件,返回模板对象
    temp = loader.get_template('static_index.html')
    # 2.模板渲染
    static_index_html = temp.render(context)

    # 生成首页对应静态文件
    save_path = os.path.join(settings.BASE_DIR, 'static/index.html')
    with open(save_path, 'w',encoding='utf-8') as f:
        f.write(static_index_html)