from django.urls import path
from task_manager.users import views

urlpatterns = [
    path("", views.user_list, name="user_list"),
    path("create/", views.user_create, name="registration"),
    path("<int:pk>/update/", views.user_update, name="update_user"),
    path("<int:pk>/delete/", views.user_delete, name="delete_user"),
]
