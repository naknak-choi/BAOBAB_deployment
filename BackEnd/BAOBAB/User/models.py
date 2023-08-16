from django.db import models
from django.conf import settings

from django.contrib.auth.models import AbstractBaseUser

from .managers import UserManager
from core.models import TimestampedModel

class User(AbstractBaseUser, TimestampedModel):
    id = models.AutoField(primary_key=True)
    
    email = models.EmailField(max_length=50, unique=True)
    username = models.CharField(max_length=50, unique=True)
    nickname = models.CharField(max_length=50, unique=True)
    
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # 로그인시 id로 사용할 필드 지정
    USERNAME_FIELD = 'email'
    # 필수로 받을 필드 지정
    REQUIRED_FIELDS = ['username', 'nickname']
    
    objects = UserManager()
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    def __str__(self):
        return self.username