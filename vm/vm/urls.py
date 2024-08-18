# vm/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('vmapp.urls')),
    path('register_user/', include('register_user.urls')),
    path('password_reset/', include('register_user.urls')),

]

