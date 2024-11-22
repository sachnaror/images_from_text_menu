# app1/admin.py
from django.contrib import admin
from .models import Menu, Dish, MenuImage

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at')

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'menu', 'description')


@admin.register(MenuImage)
class MenuImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'menu_image', 'uploaded_at']
