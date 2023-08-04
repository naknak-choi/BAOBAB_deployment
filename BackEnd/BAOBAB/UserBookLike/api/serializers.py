from rest_framework import serializers

from UserBookLike.models import UserBookLike
from Book.models import BookInfo
    
class UserBookLikeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBookLike
        fields = ['list_id']

    def create(self, validated_data):
        book_id = self.context.get('book_id')
        user_id = self.context.get('user_id')
        
        book = BookInfo.objects.get(book_id=book_id)

        user_book_like = UserBookLike.objects.create(
            user_id=user_id,
            book_id=book
        )
        return user_book_like
    
class UserBookLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBookLike
        fields = '__all__'