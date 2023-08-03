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
