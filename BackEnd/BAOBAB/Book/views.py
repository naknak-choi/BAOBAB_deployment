from .api.serializers import *

from User.api.serializers import *

from Category.models import Category

from Book.models import BookInfo

from BookRating.api.serializers import BookRatingUserSerializer
from BookRating.models import BookRating

from Comment.api.serializers import CommentInfoSerializer
from Comment.models import CommentInfo

from rest_framework import viewsets
from rest_framework.views import APIView

from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny

from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import *

class BookStaffView(APIView):
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
        
        page = 1
        for image in uploded_pages:
            page_serializer = BookFileSerializer(data={'page_image': image, 'book_id': book.book_id, 'page': page})
            page += 1
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
        book = BookInfo.objects.get(book_id=kwargs.get('book_id'))
        book.delete()
        return Response({"message": "삭제 성공"}, status=status.HTTP_200_OK)
    
    def put(self, request, *args, **kwargs):
        book = BookInfo.objects.filter(book_id=kwargs.get('book_id')).first()
        if book is None:
            return Response({"message": "존재하지 않는 책입니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        book_serializer = BookStaffSerializer(book, data=request.data, partial=True)
        if book_serializer.is_valid():
            book_serializer.save()
        else:
            return Response(book_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
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
    
    def retrieve(self, request, *args, **kwargs):
        book_id = kwargs.get('pk')
        book = BookInfo.objects.filter(book_id=book_id).first()
        if book is None:
            return Response({"message": "존재하지 않는 책입니다."}, status=status.HTTP_400_BAD_REQUEST)
        else :
            book.views += 1
            return Response(self.serializer_class(book).data, status=status.HTTP_200_OK)
    
class BookRatingListView(APIView):
    serializer_class = BookRatingUserSerializer
    
    def get(self, request, *args, **kwargs):
        book_id = kwargs.get('book_id')
        
        book = BookInfo.objects.filter(book_id=book_id).first()
        if book is None:
            return Response({"message": "존재하지 않는 책입니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        rating_list = BookRating.objects.filter(book_id=book_id)
        return Response(self.serializer_class(rating_list, many=True).data, status=status.HTTP_200_OK)
    
class BookCommentListView(APIView):
    serializer_class = CommentInfoSerializer
    
    def get(self, request, *args, **kwargs):
        book_id = kwargs.get('book_id')
        
        book = BookInfo.objects.filter(book_id=book_id).first()
        if book is None:
            return Response({"message": "존재하지 않는 책입니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        comment_list = CommentInfo.objects.filter(book_id=book_id)
        return Response(self.serializer_class(comment_list, many=True).data, status=status.HTTP_200_OK)
    
class BookPageListView(APIView):
    serilalizer_class = BookFileSerializer
    
    def get(self, request, *args, **kwargs):
        book_id = kwargs.get('book_id')
        
        book = BookInfo.objects.filter(book_id=book_id).first()
        if book is None:
            return Response({"message": "존재하지 않는 책입니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        page_list = BookFile.objects.filter(book_id=book_id)
        return Response(self.serilalizer_class(page_list, many=True).data, status=status.HTTP_200_OK)