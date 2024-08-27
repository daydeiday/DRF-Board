# posts/url.py

from django.urls import path
from rest_framework import routers
from posts.views import PostViewSet, like_post, CommentViewSet, like_comment

router = routers.SimpleRouter()
router.register('', PostViewSet)
router.register('comments', CommentViewSet)
urlpatterns = router.urls + [
  path('like/<int:pk>/', like_post, name='like_post'),
]