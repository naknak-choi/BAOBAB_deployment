from rest_framework import serializers

from UserBookLike.models import UserBookLike
from Book.models import BookInfo
    
class UserBookLikePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBookLike
        fields = ['list_id']

    def create(self, validated_data):
        book_id = self.context.get('book_id')
        user = self.context.get('user')
        
        book = BookInfo.objects.get(book_id=book_id)

        user_book_like = UserBookLike.objects.create(
            user_id=user,
            book_id=book
        )
        return user_book_like
    
class UserBookLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBookLike
        fields = '__all__'