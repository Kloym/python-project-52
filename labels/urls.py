from django.urls import path
from labels import views

urlpatterns = [
    path('', views.label_list, name='label_list'),
    path('create/', views.create_label, name='create_label'),
    path('<int:pk>/update/', views.label_update, name='update_label'),
    path('<int:pk>/delete/', views.label_delete, name='delete_label'),
]