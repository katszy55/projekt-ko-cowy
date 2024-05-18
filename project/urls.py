"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from registration_slot import views
from django.contrib.auth.views import LoginView
from registration_slot.views import reserve_slot, register, show_reserved_slot, show_all_reserved_slots, custom_logout
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    # path('login/', login_view, name='login'),
    path('login/', LoginView.as_view(), name='login'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
    path('reserve-slot/', reserve_slot, name='reserve_slot'),
    path('register/', register, name='register'),
    path('show-reserved-slot/', show_reserved_slot, name='show_reserved_slot'),
    path('all_slots', show_all_reserved_slots, name='all_slots'),
    path('logout/', custom_logout, name='logout'),
    path('password_reset_confirm/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),


]
