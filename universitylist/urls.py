from django.urls import path
import re
from django.conf.urls import url
from . import views

app_name = 'universitylist'
urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),## 根据view.后面的参数确定对应的视图， path('', views.index, name='index'，这样也可以
    path('ajax', views.ajax, name='ajax'),
    path('<int:university_id>/', views.detail, name='detail'),
]