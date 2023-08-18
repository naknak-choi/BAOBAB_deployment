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
    cover_image = BookCoverSerializer(source='bookcover', read_only=True)
    class Meta:
        model = BookInfo
        fields = '__all__'
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        # 첫 페이지 이미지 및 페이지 수 구하기
        first_page = BookFile.objects.filter(book_id=instance.book_id).first()
        total_pages = BookFile.objects.filter(book_id=instance.book_id).count()
        
        # 직렬화된 출력에 페이지 이미지 및 페이지 수 추가하기
        if first_page:
            first_page_serializer = BookFileSerializer(first_page)
            data['page_image'] = first_page_serializer.data['page_image']
            print(type(data['page_image']))
        else:
            data['page_image'] = None
        data['total_page'] = total_pages

        page_image = BookCover.objects.filter(book_id=instance.book_id).first()
        
        if page_image:
            page_image_serializer = BookCoverSerializer(page_image)
            data['cover_image'] = page_image_serializer.data['book_cover']
            
        return data