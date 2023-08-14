from BookRating.models import BookRating

from rest_framework import serializers

class BookRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookRating
        fields = ['rating_id', 'rating', 'review']
        
class BookRatingUserSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField(source='user_id.user_id')
    class Meta:
        model = BookRating
        fields = ['rating_id', 'user_id', 'rating', 'review']