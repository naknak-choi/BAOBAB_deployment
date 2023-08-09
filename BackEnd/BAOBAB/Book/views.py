from .api.serializers import *
from User.api.serializers import *
from Category.models import Category

from rest_framework import generics
from rest_framework import viewsets
from rest_framework.views import APIView

from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny

from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView

from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import *

class BookStaffView(APIView):
    queryset = BookInfo.objects.all()
    serializer_class = BookStaffSerializer
    parser_classes = [MultiPartParser, FileUploadParser]
    # permission_classes = [IsAdminUser]
    
    def post(self, request, *args, **kwargs):
        uploded_pages = request.FILES.getlist('page_image')
        if not uploded_pages:
            return Response({"message": "파일이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        book_cover_image = request.FILES.get('book_cover')
        if not book_cover_image:
            return Response({"message": "표지가 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
        main_Category = Category.objects.get(category_id=request.data['mainCategory'])
        sub_Category = Category.objects.get(category_id=request.data['subCategory'])
        book = BookInfo.objects.create(
            book_name = request.data['book_name'],
            author = request.data['author'],
            publication_year = request.data['publication_year'],
            book_status = request.data['book_status'],
            is_popular = request.data['is_popular'],
            mainCategory = main_Category,
            subCategory = sub_Category,
        )
        
        page_num = 1
        for image in uploded_pages:
            page_serializer = BookFileSerializer(data={'page_image': image, 'book_id': book.book_id, 'page_num': page_num})
            page_num += 1
            if page_serializer.is_valid():
                page_serializer.save()
            else:
                return Response(page_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        cover_serializer = BookCoverSerializer(data={'book_cover': book_cover_image, 'book_id': book.book_id})
        if cover_serializer.is_valid():
            cover_serializer.save()
        else:
            return Response(cover_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"message": "업로드 성공"}, status=status.HTTP_201_CREATED)
    
    def delete(self, request, *args, **kwargs):
        book = BookInfo.objects.get(book_id=kwargs.get('pk'))
        book.delete()
        return Response({"message": "삭제 성공"}, status=status.HTTP_200_OK)
    
    def put(self, request, *args, **kwargs):
        book = BookInfo.objects.get(book_id=request.data['book_id'])
        book_cover_image = request.FILES.get('book_cover')
        if book_cover_image:
            cover_serializer = BookCoverSerializer(data={'book_cover': book_cover_image, 'book_id': book.book_id})
            if cover_serializer.is_valid():
                cover_serializer.save()
            else:
                return Response(cover_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "수정 성공"}, status=status.HTTP_200_OK)
    
class BookUserView(viewsets.ModelViewSet):
    queryset = BookInfo.objects.all()
    serializer_class = BookUserSerializer
    permission_classes = [AllowAny]