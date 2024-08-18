from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('login', views.login, name='login'),
    path('home', views.home, name='home'),
    path('forgot_password', views.forgot_password, name='forgot_password'),
    path('api/upload_file/', views.upload_file, name='upload_file'),
    path('api/vmonline4/step/', views.call_vmonline4_step, name='call_vmonline4_step'),
    path('api/vmonline4/reset/', views.call_vmonline4_reset, name='call_vmonline4_reset'),
    path('api/vmonline4/run/', views.call_vmonline4_run, name='call_vmonline4_run'),
    path('api/vmonline4/load/', views.call_vmonline4_load, name='call_vmonline4_load'),
    path('api/vmonline4/update_memory/', views.call_vmonline4_update_memory, name='call_vmonline4_update_memory'),
]
