# users/views.py
# [1단계] - 회원가입
from django.contrib.auth.models import User
from rest_framework import generics

from .serializers import RegisterSerializer
# [2단계] - 로그인
from rest_framework import status
from rest_framework.response import Response

from .serializers import LoginSerializer

# [3단계] - User 모델 확장 - Profile
from .serializers import ProfileSerializer
from .models import Profile


# VIEW - 회원가입
class RegisterView(generics.CreateAPIView): # generics의 CreateAPIView 상속하여 구현한다.
  queryset = User.objects.all()
  serializer_class = RegisterSerializer

# VIEW - 로그인
''' 로그인 뷰 설명
    로그인의 경우 아예 MODEL과 관련이 없다고 봐도 무방하다.
    로그인의 프로세스 (토큰&JWT 방식)에 의하면 사용자가 ID/PW를 적어서 보내줬을 때,
    이를 확인하여 그에 해당하는 토큰을 응답하기만 하면 된다.
    => 따라서,
    이 작업들을 위해 ModelSerializer를 사용하지 않았으며,
      모델에 영향을 주지 않기 때문에,
      어떤 특별한 제네릭을 사용하지 않고 기본 GenericAPIView를 사용하여 간단히 구현할 수 있다.
'''
class LoginView(generics.GenericAPIView):
  serializer_class = LoginSerializer

  def post(self, request):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    token = serializer.validated_data
    return Response({"token": token.key}, status=status.HTTP_200_OK)


# VIEW - User모델 확장 Profile
class ProfileView(generics.RetrieveUpdateAPIView): # 조회 기능 + 수정기능
  queryset = Profile.objects.all()
  serializer_class = ProfileSerializer