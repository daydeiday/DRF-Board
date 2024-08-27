# todo/models.py
from django.db import models
# from django.contrib.auth.models import User
from users.models import Profile

class Todo(models.Model):
  # author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todos')
  # profile = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True)
  title = models.CharField(max_length=100)
  description = models.TextField(blank=True)
  created = models.DateTimeField(auto_now_add=True)
  complete = models.BooleanField(default=False)
  important = models.BooleanField(default=False)

  def __str__(self):
    return self.title
