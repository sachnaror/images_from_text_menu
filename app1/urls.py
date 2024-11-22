from django.urls import path
from . import views

app_name = 'app1'

urlpatterns = [
    path('', views.upload_menu, name='upload_menu'),  # Home page to upload menu
    path('menu-result/', views.menu_result, name='menu_result'),  # Page to display results
]
