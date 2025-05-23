from django.urls import path
from statuses import views

urlpatterns = [
    path("", views.status_list, name="status_list"),
    path("create/", views.create_status, name="create_status"),
    path("<int:pk>/update/", views.status_update, name="update_status"),
    path("<int:pk>/delete/", views.status_delete, name="delete_status"),
]
