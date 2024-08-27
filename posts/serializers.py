# posts/serializers.py
from rest_framework import serializers

from users.serializers import ProfileSerializer
from posts.models import Post, Comment

# Comment 모델 시리얼라이저
class CommentSerializer(serializers.ModelSerializer):
  profile = ProfileSerializer(read_only=True)
  class Meta:
    model = Comment
    fields = ("pk", "profile", "post", "text", "published_date", "likes") #pk는 상속받은 models.Model클래스에서 기본적으로 존재하는 필드이다..

class CommentCreateSerializer(serializers.ModelSerializer):
  class Meta:
    model = Comment
    fields = ("post", "text")

# Post 모델 시리얼라이저
class PostSerializer(serializers.ModelSerializer):
  # profile 필드를 따로 정의하는 이유: 이를 작성하지 않으면 기본적으로 profile 필드에는 profile의 pk값만 나타나게 된다.
  profile = ProfileSerializer(read_only=True) #nested serializer
  # 댓글 시리얼라이저를 포함하여 댓글 추가, many=True를 통해 다수의 댓글 포함
  #   즉.. Post 모델을 직렬화하면서 Comment 모델 직렬화까지 포함한다는 뜻...
  comments = CommentSerializer(many=True, read_only=True) # nested serializer
  class Meta:
    model = Post
    fields = ("pk", "author", "profile", "category", "question", "title", "body", "image", "published_date", "likes", "comments")

class PostCreateSerializer(serializers.ModelSerializer):
  class Meta:
    model = Post
    fields = ("title", "category", "body", "image")