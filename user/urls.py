from django.urls import path
from django.conf.urls import url
from . import views
app_name = 'user'
urlpatterns = [
    # url(r'^register$', views.RegisterView.as_view(), name='register'), # ע��
   #path(r'register/', views.register, name='register'),
    #path(r'detail', views.detail, name='detail'),
    path('', views.UserInfoView.as_view(), name='userinfo'), # 用户中心-信息页
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/',    views.LoginView.as_view(), name='login'),
    path('logout/',    views.LogoutView.as_view(), name='logout'),
    path('active/<str:token>',views.ActiveView.as_view(), name='active'), # �û�����
]