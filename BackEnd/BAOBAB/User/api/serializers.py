from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from User.models import User

class UserRegisterSerializer(RegisterSerializer):
    nickname = serializers.CharField(required=True)
    
    class Meta:
        model = User
        fields = ('email', 'username', 'nickname','password1', 'password2')
        
    # def create(self, validated_data):
    #     user = User.objects.create(
    #         email = validated_data['email'],
    #         username = validated_data['username'],
    #         nickname = validated_data['nickname'],
    #         is_active = False,
    #     )
        
    #     user.set_password(validated_data['password1'])
    #     user.save()
        
    #     return user
    
    def get_cleaned_data(self):
        data_dict = super().get_cleaned_data()
        data_dict['nickname'] = self.validated_data.get('nickname', '')
        
        return data_dict
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'