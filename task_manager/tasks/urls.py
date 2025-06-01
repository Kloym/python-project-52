from django.urls import path
from task_manager.tasks import views

urlpatterns = [
    path("", views.task_list, name="task_list"),
    path("create/", views.create_task, name="create_task"),
    path("<int:pk>/delete/", views.delete_task, name="delete_task"),
    path("<int:pk>/update/", views.update_task, name="update_task"),
    path("<int:pk>/", views.get, name="get_task"),
]
