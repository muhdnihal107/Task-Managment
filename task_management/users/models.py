from django.db import models
from django.contrib.auth.models import User

class UserAssignment(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_users')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_to')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('admin', 'user')

    def __str__(self):
        return f"{self.user.username} assigned to {self.admin.username}"