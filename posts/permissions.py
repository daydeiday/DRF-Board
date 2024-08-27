# posts/permissions.py
from rest_framework import permissions


'''class CustomReadOnly(permissions.BasePermission):
  ## 글 조회: 누구나 / 생성: 로그인한 유저 / 편집: 글 작성자
  def has_permission(self, request, view): #객체별 권한 뿐만 아니라 전체 객체에 대한 권한도 포함해야 하기 때문에 목록조회/생성하는 has_permission() 정의했다.
    if request.method == 'GET':
      return True
    return request.user.is_authenticated
  def has_object_permission(self, request, view, obj):
    if request.method in permissions.SAFE_METHODS:
      return True
    return obj.author == request.user
'''

class CustomReadOnly(permissions.BasePermission):
  ## 글 조회: 누구나, 생성: 로그인한 유저, 편집: 글 작성자
  def has_permission(self, request, view):
      if request.method == 'GET':
          return True
      return request.user.is_authenticated

  def has_object_permission(self, request, view, obj):
      if request.method in permissions.SAFE_METHODS:
          return True
      return obj.author == request.user