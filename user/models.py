from django.db import models
from django.contrib.auth.models import AbstractUser
from db.base_model import BaseModel
# Create your models here.                                                  


class User(AbstractUser, BaseModel):
    more_informations=models.CharField(max_length=50,null=True)
    #username = models.CharField(max_length=50,unique=True)
    #email = models.CharField(max_length=50)
    #password = models.CharField(max_length=50)
    #create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')  # verbose_name来设置详细名称
    #update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    #is_delete = models.BooleanField(default=False, verbose_name='删除标记')
    #is_active = models.BooleanField(default=False, verbose_name='激活标记')
    class Meta:
        db_table = 'user'
        verbose_name = 'my_user'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.username