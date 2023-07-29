from django.db import models
from django.conf import settings

from django.contrib.auth.models import AbstractBaseUser

from .managers import UserManager
from core.models import TimestampedModel

import jwt
from datetime import datetime, timedelta

# Create your models here.

class User(AbstractBaseUser, TimestampedModel):
    id = models.AutoField(primary_key=True)
    
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    nickname = models.CharField(max_length=50, unique=True)
    
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # 로그인시 id로 사용할 필드 지정
    USERNAME_FIELD = 'email'
    # 필수로 받을 필드 지정
    REQUIRED_FIELDS = ['username', 'nickname']
    
    object = UserManager()
    
    def __str__(self):
        return self.username
    
    @property
    
    def token(self):
        return self._generate_jwt_token( )

    def _generate_jwt_token(self):
        dt = datetime.now( ) + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': dt.utcfromtimestamp(dt.timestamp())
        }, settings.SECRET_KEY, algorithm='HS256')
        
        return token
    
class UserImage(models.Model):
    id = models.AutoField(primary_key=True)
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='user_images/', blank=True, null=True)