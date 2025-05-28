from django.db import models
from django.contrib.auth.models import User
from task_manager.statuses.models import Status
from task_manager.labels.models import Label


class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    labels = models.ManyToManyField(Label)
    author = models.ForeignKey(
        User, related_name="task_created", on_delete=models.CASCADE, default=1
    )
    assignee = models.ForeignKey(
        User, related_name="task_assigned", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# Create your models here.
