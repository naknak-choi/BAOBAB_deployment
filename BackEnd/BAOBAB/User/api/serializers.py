from rest_framework import serializers
from User.models import User
from django.utils import timezone
from django.contrib.auth import authenticate


class RegistrationSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(
        max_length = 128,
        min_length = 8,
        write_only = True
    )
    
    token = serializers.CharField(max_length=255, read_only=True)
    
    class Meta:
        model = User
        fields = [
            'email', 
            'username',
            'nickname',
            'password',
            'token',
            ]
        
    def create(self, validated_data):
        return User.object.create_user(**validated_data)
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    # 1.
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    last_login = serializers.CharField(max_length=255, read_only=True)
    
    # 2.
    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)
        
        # 3.
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )
        
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )
        
        # 4.
        user = authenticate(username=email, password=password)
        
        # 5.
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found'
            )
        
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )
        
        # 6.
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])
        
        # 7.
        return {
            'email': user.email,
            'username': user.username,
            'last_login': user.last_login
        }
        

class UserSerializer(serializers.ModelSerializer):
    
    # 2.
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    
    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'password',
            'token'
        ]
        
        # 3.
        read_only_fields = ('token', )
        
    # 4.
    def update(self, instance, validated_data):
        # 5.
        password = validated_data.pop('password', None)
        
        # 6.
        for (key, value) in validated_data.items():
            # 7.
            setattr(instance, key, value)

        if password is not None:
            # 8.
            instance.set_password(password)

        # 9.
        instance.save()

        return instance       
from rest_framework import serializers

from User.models import User
from UserBookLike.api.serializers import UserBookLikeSerializer

class UserSerializer(serializers.ModelSerializer):
    user_book_like = UserBookLikeSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }
