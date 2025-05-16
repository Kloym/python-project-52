from django.db import models
from django.contrib.auth.models import User
from statuses.models import Status

class Task(models.Model):
    name = models.CharField(max_length=100)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='task_created', on_delete=models.CASCADE)
    assignee = models.ForeignKey(User, related_name='task_assigned', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
# Create your models here.
