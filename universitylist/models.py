import datetime
from django.db import models
from db.base_model import BaseModel
from django.utils import timezone
# Create your models here.

# https://country-code.cl/
class Continent(models.Model):
    name = models.CharField(max_length=50,unique=True)
    short_name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Country(BaseModel):
    name = models.CharField(max_length=50,unique=True)
    continent=models.ForeignKey(Continent,on_delete=models.CASCADE)    #models.CASCADE, 删除关联数据,与之关联也删除  
    short_name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
   
class University(models.Model):
    name = models.CharField(max_length=1000)
    latest_rank = models.IntegerField()
    city = models.CharField(max_length=50,default=None,null=True)
    country=models.CharField(max_length=50,default=None,null=True)   
    address = models.CharField(max_length=500,default=None)
    website = models.CharField(max_length=500,default=None,null=True)
    summary = models.CharField(max_length=10000,default=None,null=True)
    longitude=models.FloatField(default=None,null=True)
    latitude = models.FloatField(default=None,null=True)
    date_url=models.CharField(max_length=1000,default=None)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')  # verbose_name来设置详细名称
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    def __str__(self):
        return self.name

class University_more(models.Model):
    name = models.CharField(max_length=1000)
    key = models.CharField(max_length=500,null=True)
    value = models.CharField(max_length=100,null=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')  # verbose_name来设置详细名称
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    def __str__(self):
        return self.name+"_more"

class University_indicator_and_subject_rankings(models.Model):
    name = models.CharField(max_length=1000)
    key = models.CharField(max_length=500,null=True)
    value = models.CharField(max_length=100,null=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')  # verbose_name来设置详细名称
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    def __str__(self):
        return self.name+"_indicator_and_subject_rankings"



class Project(models.Model):
    name = models.CharField(max_length=500)
    #universty= models.ForeignKey(University, on_delete=models.CASCADE)
    TOEFL = models.IntegerField(null=True)
    IELTS = models.IntegerField(null=True)
    GRE = models.IntegerField()
    tuition = models.IntegerField()
    degree = models.CharField(max_length=50)
    time_required=models.IntegerField()
    url =  models.URLField(max_length=200)
    def __str__(self):
        return self.name


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        return self.pub_date>=timezone.now - datetime.timedelta(days=1)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text



# 根据国家排名查找大学综合排名
# 根据专业查找在某一国家大学排名
