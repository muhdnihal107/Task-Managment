from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    STATUS_CHOICES = [
        ('pending','Pending'),
        ('in_progress','In Progress'),
        ('completed','Completed'),
        ]
    title = models.CharField(max_length=100)
    description = models.TextField()
    assigned_to = models.ForeignKey(User,on_delete=models.CASCADE,related_name='tasks')
    due_date = models.DateField()
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='Pending')
    completion_report = models.TextField(blank=True, null=True)
    worked_hours = models.FloatField(blank=True,null=True)
