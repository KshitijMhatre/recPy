from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.index ,name='movierec'),
    path('login/',views.login ,name='login'),

]

