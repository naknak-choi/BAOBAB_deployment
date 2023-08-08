from rest_framework import serializers
from Book.models import *

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
    book_file = serializers.FileField(write_only=True, required = False)
    book_cover = serializers.ImageField(write_only=True, required = False)
    
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
        book.clean()
        BookFile.objects.create(book_id=book, book_file=book_file_data)
        BookCover.objects.create(book_id=book, book_cover=book_cover_data)

        return book

    def update(self, instance, validated_data):
        instance.clean()
        book_file = validated_data.pop('book_file', None)
        book_cover = validated_data.pop('book_cover', None)

        if book_file:
            bookfile_instance = BookFile.objects.get_or_create(book_id=instance)
            bookfile_instance.book_file = book_file
            bookfile_instance.save()

        if book_cover:
            bookcover_instance = BookCover.objects.get_or_create(book_id=instance)
            bookcover_instance.book_cover = book_cover
            bookcover_instance.save()

        return super(BookStaffSerializer, self).update(instance, validated_data)
    
class BookUserSerializer(serializers.ModelSerializer):
    book_file = BookFileSerializer(source='bookfile', read_only=True)
    book_cover = BookCoverSerializer(source='bookcover', read_only=True)
    class Meta:
        model = BookInfo
        fields = '__all__'