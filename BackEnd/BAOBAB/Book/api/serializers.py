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
        
# BookInfo 정보 + 관련된 BookFile, BookCover 정보를 한번에 보여주기 위한 Serializer
class BookStaffSerializer(serializers.ModelSerializer):
    # create시 book_file, book_cover를 받기 위한 write_only 필드
    book_file = serializers.FileField(write_only=True)
    book_cover = serializers.ImageField(write_only=True)
    
    # book_file, book_cover를 보여주기 위한 read_only 필드
    book_file_data = BookFileSerializer(source='bookfile', read_only=True)
    book_cover_data = BookCoverSerializer(source='bookcover', read_only=True)
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
class BookUserSerializer(serializers.ModelSerializer):
    book_file_data = BookFileSerializer(source='bookfile', read_only=True)
    book_cover_data = BookCoverSerializer(source='bookcover', read_only=True)
    class Meta:
        model = BookInfo
        fields = '__all__'

class BookRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookStats
        fields = ['average_rating']