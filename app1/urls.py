# app1/urls.py
from django.urls import path
from . import views

app_name = 'app1'  # This should appear only once

urlpatterns = [
    path('', views.upload_menu, name='upload_menu'),
    path('menu-result/', views.menu_result, name='menu_result'),
]
