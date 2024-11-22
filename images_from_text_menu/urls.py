from django.contrib import admin
from django.urls import path, include  # Include for app URLs
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app1.urls')),  # Routes for menu_images_app
    path('app1/', include('app1.urls')),  # Routes for cssapp1
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
