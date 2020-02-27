from django.urls import path,include
import re
from django.conf.urls import url
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
router = DefaultRouter()
# router.register(r'api','universitylist',views.Api,basename="api") 
router.register('api',views.Api) 
router.register('bpi',views.Bpi)   #所以如果viewset类(第二个参数)中没用queryset属性，必须设置basename
app_name = 'universitylist'
urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    ## 根据view.后面的参数确定对应的视图， path('', views.index, name='index'，这样也可以
    url('api/', include(router.urls)),
    path('ajax', views.ajax, name='ajax'),
    #path('api/', views.Api.as_view(), name='api'),
    path('universitylist/<int:university_id>/', views.detail, name='detail'),
]
urlpatterns += router.urls