"""
URL configuration for task_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from my_task_manager import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.index, name='index'),
    path('users/', views.user_list, name='user_list'),
    path('users/create/', views.user_create, name='registration'),
    path('login/', views.login_view, name='login'),
    path('home/', views.login_index, name='login_index'),
    path('users/<int:pk>/update/', views.user_update, name='update_user'),
    path('users/<int:pk>/delete/', views.user_delete, name='delete_user'),
    path('logout/', views.logout_view, name='logout'),
    path('statuses/', views.status_list, name='status_list'),
    path('statuses/create/', views.create_status, name='create_status'),
    path('statuses/<int:pk>/delete/', views.status_delete, name='delete_status'),
    path('statuses/<int:pk>/update/', views.status_update, name='update_status'),
]
