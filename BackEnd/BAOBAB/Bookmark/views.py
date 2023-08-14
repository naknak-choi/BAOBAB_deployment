from .api.serializers import BookmarkSerializer
from .models import Bookmark

from Book.models import BookFile, BookInfo

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

class BookmarkListCreate(generics.ListCreateAPIView):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    
class BookmarkDestroy(generics.DestroyAPIView):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    
class BookmarkView(BookmarkListCreate, BookmarkDestroy):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    
    def post(self, request, *args, **kwargs):
        user_id = request.user
        page = request.data.get('page')
        book_id = kwargs.get('book_id')
        book = BookInfo.objects.get(book_id=book_id)
        if book is None:
            return Response({"error":"존재하지 않는 책입니다."},status=status.HTTP_400_BAD_REQUEST)
        
        file = BookFile.objects.get(book_id=book_id, page = page)
        
        bookmark = Bookmark.objects.filter(user_id=user_id, book_id=book, file_id=file)
        if bookmark.exists():
            return Response({"error" : "이미 북마크를 추가한 페이지입니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        new_bookmark = Bookmark.objects.create(user_id=user_id, book_id=book, file_id=file)
        return Response(BookmarkSerializer(new_bookmark).data, status=status.HTTP_200_OK)
    
    def delete(self, request, *args, **kwargs):
        user_id = request.user
        page = request.data.get('page')
        book_id = kwargs.get('book_id')
        book = BookInfo.objects.get(book_id=book_id)
        if book is None:
            return Response({"error":"존재하지 않는 책입니다."},status=status.HTTP_400_BAD_REQUEST)
        
        file = BookFile.objects.get(book_id=book_id, page = page)
        
        bookmark = Bookmark.objects.filter(user_id=user_id, book_id=book, file_id=file)
        if not bookmark.exists():
            return Response({"error" : "북마크가 존재하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        bookmark.delete()
        return Response({"success" : "북마크가 삭제되었습니다."}, status=status.HTTP_200_OK)
    
    def get(self, request, *args, **kwargs):
        user_id = request.user
        book_id = kwargs.get('book_id')
        book = BookInfo.objects.get(book_id=book_id)
        if book is None:
            return Response({"error":"존재하지 않는 책입니다."},status=status.HTTP_400_BAD_REQUEST)
        
        bookmarks = Bookmark.objects.filter(user_id=user_id, book_id=book)
        if not bookmarks.exists():
            return Response({"error" : "북마크가 존재하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(BookmarkSerializer(bookmarks, many=True).data, status=status.HTTP_200_OK)