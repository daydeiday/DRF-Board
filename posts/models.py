from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from users.models import Profile
# 게시글 모델
class Post(models.Model):
  author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
  profile = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True)
  title = models.CharField(max_length=128)
  category = models.CharField(max_length=128)
  question = models.BooleanField(default=False)
  body = models.TextField()
  image = models.ImageField(upload_to='post/', default='default.jpg')
  likes = models.ManyToManyField(User, related_name='like_posts', blank=True)
  published_date = models.DateTimeField(default=timezone.now)

# 댓글 모델 
class Comment(models.Model):
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
  post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
  text = models.TextField()
  likes = models.ManyToManyField(User, related_name='like_comments', blank=True)
  published_date = models.DateTimeField(default=timezone.now)