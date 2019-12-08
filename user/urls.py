from django.urls import path
from django.conf.urls import url
from . import views
app_name = 'user'
urlpatterns = [
    # url(r'^register$', views.RegisterView.as_view(), name='register'), # ×¢²á
   #path(r'register/', views.register, name='register'),
    #path(r'detail', views.detail, name='detail'),
    path(r'register/', views.RegisterView.as_view(), name='register'),
    path(r'login/',    views.LoginView.as_view(), name='login'),
    path(r'active/<str:token>',views.ActiveView.as_view(), name='active'), # ÓÃ»§¼¤»î
]