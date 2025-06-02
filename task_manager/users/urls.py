from django.urls import path
from task_manager.users import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="user_list"),
    path("create/", views.UserCreateView.as_view(), name="registration"),
    path("<int:pk>/update/", 
        views.UserUpdateView.as_view(), 
        name="update_user"
        ),
    path("<int:pk>/delete/", 
        views.UserDeleteView.as_view(), 
        name="delete_user"
        ),
]
