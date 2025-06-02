from django.contrib.auth.models import User
from django.db import models
from task_manager.statuses.models import Status


class Task(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    author = models.ForeignKey(User, 
                               on_delete=models.CASCADE, 
                               related_name='tasks_created')
    executor = models.ForeignKey(User, 
                                 on_delete=models.PROTECT, 
                                 null=True, blank=True, 
                                 related_name='tasks_assigned')
    labels = models.ManyToManyField('labels.Label', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


# Create your models here.
