from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class ChatLog(models.Model):
    USER_ROLES = (
        ('admin', 'Administrator'),
        ('student', 'Student'),
        ('lecturer', 'Lecturer'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=USER_ROLES)
    query = models.TextField()
    response = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    context = models.JSONField(default=dict, blank=True)  # For storing additional context

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user.username} ({self.role}) - {self.timestamp}"

class UserPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_role = models.CharField(
        max_length=10,
        choices=ChatLog.USER_ROLES,
        default='student'
    )
    enable_notifications = models.BooleanField(default=True)
    theme = models.CharField(max_length=20, default='light')

    def __str__(self):
        return f"{self.user.username}'s preferences"