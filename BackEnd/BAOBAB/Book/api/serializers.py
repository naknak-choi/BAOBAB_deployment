from rest_framework import serializers
from Book.models import *
from User.models import *

class BookFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookFile
        fields = ['book_file']
        
class BookCoverSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCover
        fields = ['book_cover']

class CreateBookSerializer(serializers.ModelSerializer):
    book_file = serializers.FileField(write_only=True)
    book_cover = serializers.ImageField(write_only=True)

    class Meta:
        model = BookInfo
        fields = '__all__'

    def create(self, validated_data):
        book_file_data = validated_data.pop('book_file')
        book_cover_data = validated_data.pop('book_cover')

        book = BookInfo.objects.create(**validated_data)
        BookFile.objects.create(book_id=book, book_file=book_file_data)
        BookCover.objects.create(book_id=book, book_cover=book_cover_data)
        BookStats.objects.create(book_id=book)

        return book

class ListUpBookSerializer(serializers.ModelSerializer):
    book_file = BookFileSerializer(source='bookfile')
    book_cover = BookCoverSerializer(source='bookcover')

    class Meta:
        model = BookInfo
        fields = '__all__'

class BookRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookStats
        fields = ['average_rating']