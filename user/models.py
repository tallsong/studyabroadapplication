from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.                                                  
class BaseModel(models.Model):
    '''模型抽象基类'''
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_delete = models.BooleanField(default=False, verbose_name='删除标记')

    class Meta:
        # 说明是一个抽象模型类
        abstract = True



class User(models.Model):
    name = models.CharField(max_length=50,unique=True)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')  # verbose_name来设置详细名称
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_delete = models.BooleanField(default=False, verbose_name='删除标记')
    def __str__(self):
        return self.name