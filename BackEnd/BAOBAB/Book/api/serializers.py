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
            ]

    # def create(self, validated_data):
    #     page_image_data = validated_data.pop('page_image',[])
    #     book_cover_data = validated_data.pop('book_cover')

    #     book = BookInfo.objects.create(**validated_data)
    #     book.clean()
    #     BookFile.objects.create(book_id=book, page_image=page_image_data)
    #     BookCover.objects.create(book_id=book, book_cover=book_cover_data)

    #     return book

    # def update(self, instance, validated_data):
    #     instance.clean()
    #     page_image = validated_data.pop('page_image', [])
    #     book_cover = validated_data.pop('book_cover', )

    #     if page_image:
    #         bookfile_instance = BookFile.objects.get_or_create(book_id=instance)
    #         bookfile_instance.page_image = page_image
    #         bookfile_instance.save()

    #     if book_cover:
    #         bookcover_instance = BookCover.objects.get_or_create(book_id=instance)
    #         bookcover_instance.book_cover = book_cover
    #         bookcover_instance.save()

    #     return super(BookStaffSerializer, self).update(instance, validated_data)
    
class BookUserSerializer(serializers.ModelSerializer):
    page_image = BookFileSerializer(source='bookfile_set', read_only=True, many = True)
    book_cover = BookCoverSerializer(source='bookcover', read_only=True)
    class Meta:
        model = BookInfo
        fields = '__all__'