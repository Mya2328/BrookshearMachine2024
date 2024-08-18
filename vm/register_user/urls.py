from django.urls import path
from . import views

urlpatterns = [
    path('register_user/', views.register_user, name='register_user'),
    path('password_reset/', views.password_reset, name='password_reset'),
]
