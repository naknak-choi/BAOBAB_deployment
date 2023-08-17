from rest_framework import serializers
from Book.models import *

class BookFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookFile
        fields = '__all__'
        
class BookCoverSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCover
        fields = '__all__'
        
# BookInfo 정보 + 관련된 BookFile, BookCover 정보를 한번에 보여주기 위한 Serializer
class BookStaffSerializer(serializers.ModelSerializer):
    page_image = serializers.ImageField(write_only=True)
    book_cover = serializers.ImageField(write_only=True)
    
    page_image_data = BookFileSerializer(source='bookfile_set', read_only=True, many = True)
    book_cover_data = BookCoverSerializer(source='bookcover', read_only=True)
    class Meta:
        model = BookInfo
        fields = [
            'book_id',
            'book_name',
            'author',
            'mainCategory',
            'subCategory',
            'publication_year',
            'book_status',
            'is_popular', 
            'created_at',
            'page_image',
            'book_cover',
            'page_image_data',
            'book_cover_data',
            'book_introduction',
            ]
    
class BookUserSerializer(serializers.ModelSerializer):
    page_image = BookFileSerializer(source='bookfile_set', read_only=True, many = True)
    book_cover = BookCoverSerializer(source='bookcover', read_only=True)
    class Meta:
        model = BookInfo
        fields = '__all__'