# vmapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/asm3/', views.call_asm3, name='call_asm3'),
    path('api/vmonline4/step/', views.call_vmonline4_step, name='call_vmonline4_step'),
    path('api/vmonline4/reset/', views.call_vmonline4_reset, name='call_vmonline4_reset'),
    path('api/vmonline4/run/', views.call_vmonline4_run, name='call_vmonline4_run'),
    path('api/vmonline4/load/', views.call_vmonline4_load, name='call_vmonline4_load'),
    path('api/upload_file/', views.upload_file, name='upload_file'),
]
