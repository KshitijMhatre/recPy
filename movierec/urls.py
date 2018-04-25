from django.contrib import admin
from django.urls import path
from . import views
import bookrec.views as bviews
from django.conf.urls import url

app_name= 'movierec'

urlpatterns = [
    path('',views.index ,name='movierec'),
    path('bookrec/',bviews.index ,name='bookrec'),
    path('login/',views.login_user ,name='login_user'),
    path('register/',views.register ,name='register'),
    path('logout/',views.logout_user ,name='logout_user'),
    path('detail/', views.detail,name='detail'),
    path('search/', views.search_movies),
    path('recommend/', views.recommend_movies),
    path('rate/', views.rate_movies),
    path('related/', views.related_movies),
    
]

