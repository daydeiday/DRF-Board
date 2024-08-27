from django.contrib import admin
from .models import Todo  # photo\models.py 의 Todo 클래스를 불러옴

# Register your models here.
admin.site.register(Todo) # admin 페이지에 Photo 모델을 등록
