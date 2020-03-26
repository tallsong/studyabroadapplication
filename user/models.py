from django.db import models
from django.contrib.auth.models import AbstractUser
from db.base_model import BaseModel
# Create your models here.                                                  


class User(AbstractUser, BaseModel):
    #晚点加进去
    country=models.CharField(max_length=50,null=True)
    school_type=models.CharField(max_length=50,null=True)
    degree = models.CharField(max_length=50,null=True)
    degree_type = models.CharField(max_length=50,null=True)
    school_rank = models.CharField(max_length=50,null=True)
    graduate_school=models.CharField(max_length=50,null=True)
    ielts=models.CharField(max_length=50,null=True)
    toefl=models.CharField(max_length=50,null=True)
    fee=models.CharField(max_length=50,null=True)
    age=models.IntegerField(null=True)
    more_informations=models.CharField(max_length=50,null=True)
    sex = models.BooleanField(null=True)
    discipline_competition=models.BooleanField(null=True)
    club_activity=models.BooleanField(null=True)
    research_experience=models.BooleanField(null=True)
    work_experience=models.BooleanField(null=True)





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