# batvoice_project/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Include your app's URL configurations
    path('api/', include('transcription')),  # Replace 'your_app_name' with the name of your Django app
    # ... other paths
]

# If you're using Django's authentication system, you might also have urlpatterns for it:
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]

# If you're in development and need to serve media files:
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
