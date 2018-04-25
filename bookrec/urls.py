from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls import url

app_name= 'bookrec'

urlpatterns = [
    path('bookrec/',views.index ,name='bookrec'),
    
]

from django.contrib import admin
from django.urls import path
from . import views
import movierec.views as mviews
from django.conf.urls import url

app_name= 'bookrec'

urlpatterns = [
    path('movierec/',mviews.index ,name='movierec'),
    path('',views.index ,name='bookrec'),
    
    path('logout/',mviews.logout_user ,name='logout_user'),
    path('detail/', views.detail,name='detail'),
    path('search/', views.search_books),
    path('recommend/', views.recommend_books),
    path('rate/', views.rate_books),
    path('related/', views.related_books),
    
]

