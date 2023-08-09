from BookRating.models import BookRating

from rest_framework import serializers

class BookRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookRating
        fields = ['rating_id', 'rating', 'review']