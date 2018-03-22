from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls import url

app_name= 'movierec'

urlpatterns = [
    path('',views.index ,name='movierec'),
    path('login/',views.login_user ,name='login_user'),
    path('register/',views.register ,name='register'),
    path('logout/',views.logout_user ,name='logout_user'),
    path('detail/', views.detail,name='detail'),
    path('search/', views.search_movies),
    path('recommend/', views.recommend_movies),
    
]

