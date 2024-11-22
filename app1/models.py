from django.db import models

class Menu(models.Model):
    title = models.CharField(max_length=255)
    menu_image = models.ImageField(upload_to='menu_images/', blank=True, null=True)  # Optional menu image
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Dish(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='dishes')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    generated_image = models.ImageField(upload_to='dish_images/', blank=True, null=True)  # Generated image

    def __str__(self):
        return self.name
