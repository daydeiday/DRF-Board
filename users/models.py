# users/models.py
''' (교재 내용) User 모델에 관하여
Django의 기본 User 모델을 사용하기 때문에 따로 모델을 만들 필요가 없습니다.
따라서, users/models.py에 작성할 내용이 없습니다.
대신 Django의 기본 모델 필드 중 아래 필드들을 다음과 같이 사용한다는 것을 미리 정의하고 넘기겠습니다.
https://docs.djangoproject.com/en/3.1/ref/contrib/auth/

--- Django 기본 유저 모델 내의 필드 ---
username: ID로 활용 | CharField(required = True)
email: 이메일주소 | EmailField(required = True)
password: 비밀번호 | CharField(required = True)

사용자는 회원가입을 할 때 위의 내용들을 필수적으로 입력해야 합니다.
이에 추가적으로 password2를 입력받게 하여 password와 일치하는지, 즉 비밀번호를 다시 확인하는 과정을 거치게끔 하겠습니다.

'''
''' (교재 내용) User 모델 확장시도

---아래 부터는 기본 유저 모델에서 추가할 필드. 모델 확장 ---
nickname: 닉네임 | CharField
position: 직종 | CharField
subjects: 관심사 | CharField
image: 프로필 이미지 | ImageField

모델 확장 방법 4가지
1. Proxy Model : 기본 User 모델을 그대로 상속받아 기능 추가|동작 변경
  - 가장 간단하게 적용, *그러나* 기존 User 모델의 스키마를 변경하지 않기 때문에 정작 우리에게 필요한 필드 추가 불가능

2. 1:1(One-To-One) Model - 채택
  - 기본 User 모델에 일대일로 연결되는 새로운 모델을 하나 만드는 방식
  - User 모델을 직접 건드리지 않으면서도 필드를 추가할 수 있는 좋은 방법
  - 단점: 두 개의 모델을 연결하여 사용하는 것 -> 한 개의 모델 사용보다 느리다. 효율적이지 않다.

  > 적용방법
    [1] Profile 모델 하나 생성
    [2] Profile 모델의 속성에 추가하고 싶은 속성들을 추가 (nickname, image, ...)
    [3] Proifle 모델에 User를 OneToOneField로 연결해주며 마무리

3. AbstractBaseUser
  - 가장 정석적인 방법 中 하나
  - User 모델을 추상화시킨 AbstractBaseUser 모델을 상속받아와 아예 새로운 유저 모델을 만드는 방식
  - 일일이 구현해야 하는 부분이 크다 => 자유도 높고, 난이도 높다
  - 프로젝트 진행 중에는 쉽게 채택하기 어렵다. 프로젝트 시작 전 충분한 고민과 계획을 갖고 채택할 만한 방식.
  - 어떨 때 유용한가? "추가적으로 구현하거나 수정할 시능이 많을 때"

4. AbstractUser
  - 기본 유저 모델을 그대로 가져와 필요한 내용만 수정하거나 추가할 수 있는 방식
  - 마찬가지로, 새로운 유저 모델을 만드는 방식
  - 가장 많이 쓰이는 방식, 편리한 방법
  - 프로젝트 초기에 채택해야 한다.
'''
'''  1:1(One-To-One) Model - 채택
  - 기본 User 모델에 일대일로 연결되는 새로운 모델을 하나 만드는 방식
  - User 모델을 직접 건드리지 않으면서도 필드를 추가할 수 있는 좋은 방법
  - 단점: 두 개의 모델을 연결하여 사용하는 것 -> 한 개의 모델 사용보다 느리다. 효율적이지 않다.

  > 적용방법
    [1] Profile 모델 하나 생성
    [2] Profile 모델의 속성에 추가하고 싶은 속성들을 추가 (nickname, image, ...)
    [3] Proifle 모델에 User를 OneToOneField로 연결해주며 마무리
'''
# [3단계] - User 모델 확장
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# from django.core.validators import MinValueValidator, MaxValueValidator

class Profile(models.Model):
  # user 속성의 primary_key를 User의 pk로 설정하여 통합적으로 관리한다.
  user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
  nickname = models.CharField(max_length=128)
  position = models.CharField(max_length=128)
  subjects = models.CharField(max_length=128)
  image = models.ImageField(upload_to='profile/', default='default.jpg')

  # gender = (
  #   ("male", "남자"),
  #   ("female", "여자"),
  #   ("other", "기타"))
  birthdate = models.DateField()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
  if created:
    Profile.objects.create(user=instance)
