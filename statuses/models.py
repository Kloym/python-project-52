from django.db import models

class Status(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        app_label = 'statuses'
# Create your models here.
