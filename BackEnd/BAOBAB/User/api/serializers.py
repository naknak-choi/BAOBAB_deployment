from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from User.models import User
from rest_framework.response import Response
from rest_framework import status

class UserRegisterSerializer(RegisterSerializer):
    nickname = serializers.CharField(required=True)
    
    class Meta:
        model = User
        fields = ('email', 'username', 'nickname','password1', 'password2')
    
    def get_cleaned_data(self):
        data_dict = super().get_cleaned_data()
        data_dict['nickname'] = self.validated_data.get('nickname', '')
        
        return data_dict
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'