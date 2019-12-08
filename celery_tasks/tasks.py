# 使用celery
from django.core.mail import send_mail
from django.conf import settings
from celery import Celery
import time

#在任务处理者一端加这几句
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studyabroadapplication.settings')
django.setup()

# 创建一个Celery类的实例对象
app = Celery('celery_tasks.tasks', broker='redis://127.0.0.1/8')


# 定义任务函数
@app.task
def send_register_active_email(to_email, username, token):
    '''发送激活邮件'''
    # 组织邮件信息
    subject = 'welcome to STUDYABROADAPPLICATION'
    message = ''
    sender = settings.EMAIL_FROM
    receiver = [email]
    html_message = '<h1>%s, welocme to join a member of STUDYABROADAPPLICATION</h1>please click the link below to active your account<br/><a href="http://127.0.0.1:8000/user/active/%s">http://127.0.0.1:8000/user/active/%s</a>' % (username, token, token)

    send_mail(subject, message, sender, receiver, html_message=html_message)
    time.sleep(5)