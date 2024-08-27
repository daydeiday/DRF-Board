# users/serializers.py
# [1단계] - 회원가입
from django.contrib.auth.models import User # Django에서 제공하는 User 모델을 가져온다.
from django.contrib.auth.password_validation import validate_password # Django의 기본 비밀번호 검증 도구
# [2단계] - 로그인
from django.contrib.auth import authenticate # Django의 기본 제공하는 authenticate 함수이다. 
# authenticate 함수는 위 코드에서 설정한 DefaultAuthBackend인 TokenAuth 방식으로 유저를 인증해준다.

from rest_framework import serializers
from rest_framework.authtoken.models import Token # DRF에서 제공하는 Token 모델을 가져온다.
from rest_framework.validators import UniqueValidator # DRF에서 제공하는 email 중복 방지를 위한 검증 도구를 가져온다.
# [3단계] - User 모델 확장
from .models import Profile


# class - 회원가입을 위한 시리얼라이저 
class RegisterSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(
    required = True,
    validators = [UniqueValidator(queryset=User.objects.all())], # email 중복 검증
  )
  password = serializers.CharField(
    write_only = True,
    required = True,
    validators = [validate_password], # 비밀번호 검증
  )
  # 비밀번호 확인을 위한 필드변수
  password2 = serializers.CharField(write_only=True, required=True)

  class Meta:
    model = User
    fields = ('username', 'password', 'password2', 'email')
  
  def validate(self, data):
    # 추가적으로 비밀번호 일치 여부를 확인함.
    if data['password'] != data['password2']:
      raise serializers.ValidationError(
        {"password": "Password fields didn't match."}
      )
    return data
  
  def create(self, validated_data):
    #create 요청에 대해 create 메소드를 오버라이딩, user를 생성하고 토큰을 생성하게 함.
    user = User.objects.create_user(
      username = validated_data['username'],
      email = validated_data['email'],
    )

    user.set_password(validated_data['password'])
    user.save()
    token = Token.objects.create(user=user)
    return user



# [2단계] - 로그인
# from django.contrib.auth import authenticate # Django의 기본 제공하는 authenticate 함수이다. 
# authenticate 함수는 위 코드에서 설정한 DefaultAuthBackend인 TokenAuth 방식으로 유저를 인증해준다.

# class - 로그인을 위한 시리얼라이저
''' 로그인 시리얼라이저 설명
    로그인의 경우 아예 MODEL과 관련이 없다고 봐도 무방하다.
    로그인의 프로세스 (토큰&JWT 방식)에 의하면 사용자가 ID/PW를 적어서 보내줬을 때,
    이를 확인하여 그에 해당하는 토큰을 응답하기만 하면 된다.
    => 따라서, 이 작업들을 위해 ModelSerializer를 사용할 필요가 없다.
'''
class LoginSerializer(serializers.Serializer):
  username = serializers.CharField(required=True)
  password = serializers.CharField(required=True, write_only=True)
  ''' password 의 write_only 옵션
      - O 클라이언트-> 서버 방향의 역직렬화 가능
      - X 서버-> 클라이언트 방향의 직렬화 불가능
  '''
  
  def validate(self, data):
    user = authenticate(**data)
    if user:
      token = Token.objects.get(user=user)
      return token
    raise serializers.ValidationError(
      {"error": "Unable to log in with provided credentials."}
    )

# [3단계] - User 모델 확장
# from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = Profile
    fields = ("nickname", "position", "subjects", "image")