from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer

from User.models import User

class CustomRegisterSerializer(RegisterSerializer):
    nickname = serializers.CharField(required = True)
    
    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2', 'nickname')
    
    def get_cleaned_data(self):
        data_dict = super().get_cleaned_data()
        print(data_dict)
        data_dict['nickname'] = self.validated_data.get('nickname', '')
        
        return data_dict
    
    # def save(self, request):
    #     user = super().save(request)
    #     user.nickname = self.validated_data["nickname"]
    #     user.save()
    #     return user