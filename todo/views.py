# todo/views.py
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import viewsets

from .models import Todo
from .serializers import TodoSimpleSerializer, TodoDetailSerializer, TodoCreateSerializer

''' Django 프로젝트의 views.py의 기존 import 코드
from django.shortcuts import render
'''

# Class based view 클래스형 뷰
class TodosAPIView(APIView):
  def get(self, request): # 전체 조회 뷰 : GET 방식으로 요청
    todos = Todo.objects.filter(complete=False) # Todo 클래스(=모델)의 객체 뽑아오기 (조건부)
    serializer = TodoSimpleSerializer(todos, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def post(self, request):
    serializer = TodoCreateSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TodoAPIView(APIView):
  def get (self, request, pk):
    todo = get_object_or_404(Todo, id=pk) # todo에 Todo 모델 객체 받아오기
    serializer = TodoDetailSerializer(todo) # 시리얼라이저에 Todo 객체 통과시키기
    return Response(serializer.data, status=status.HTTP_200_OK) # 시리얼라이저를 통과한 Todo 객체를 Response에 전달한다.

  def put(self, request, pk):
    todo = get_object_or_404(Todo, id=pk)
    serializer = TodoCreateSerializer(todo, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DoneTodosAPIView(APIView):
  def get(self, request):
    dones = Todo.objects.filter(complete=True)
    serializer = TodoSimpleSerializer(dones, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

class DoneTodoAPIView(APIView):
  #다른 메소드를 사용해도 되지만, 간단한 방식이므로 get 방식으로 작성했다고 한다.
  #수정하는 API이기 때문에 PUT 이나 PATCH와 같은 메소드를 활용할 수 있다고 한다.
  def get(self, request, pk): 
    done = get_object_or_404(Todo, id=pk)
    done.complete = True
    done.save()
    serializer = TodoDetailSerializer(done)
    return Response(status=status.HTTP_200_OK)
