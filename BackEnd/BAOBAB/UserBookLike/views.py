from .api.serializers import *
from Book.models import BookInfo

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class UserBookLikeView(APIView):
    serializer_class = UserBookLikeCreateSerializer
        
    def post(self, request, *args, **kwargs):
        user_id = self.request.user
        book_id = kwargs.get('book_id')
        
        book = BookInfo.objects.get(book_id=book_id)
        if book is None:
            return Response({"error":"존재하지 않는 책입니다."},status=status.HTTP_400_BAD_REQUEST)
        book_like = UserBookLike.objects.filter(user_id=user_id, book_id=book_id)
        if book_like.exists():
            return Response({"error" : "이미 좋아요를 누른 책입니다."}, status=status.HTTP_400_BAD_REQUEST)
        book.like += 1
        context = {
            'user_id': user_id,
            'book_id': book_id
        }
        serializer = self.serializer_class(data=request.data, context=context)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, *args, **kwargs):
        user_id = self.request.user
        book_id = kwargs.get('book_id')
        
        book = BookInfo.objects.get(book_id=book_id)
        if book is None:
            return Response({"error":"존재하지 않는 책입니다."},status=status.HTTP_400_BAD_REQUEST)
        book_like = UserBookLike.objects.filter(user_id=user_id, book_id=book_id)
        if not book_like.exists():
            return Response({"error" : "좋아요를 누르지 않은 책입니다."}, status=status.HTTP_400_BAD_REQUEST)
        book.lije -= 1
        book_like.delete()
        return Response(data={"message": "성공적으로 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)
    
    def get(self, request, *args, **kwargs):
        user_id = self.request.user
        book_id = kwargs.get('book_id')
        
        book = BookInfo.objects.get(book_id=book_id)
        if book is None:
            return Response({"error":"존재하지 않는 책입니다."},status=status.HTTP_400_BAD_REQUEST)
        book_like = UserBookLike.objects.filter(user_id=user_id, book_id=book_id)
        if not book_like.exists():
            return Response({"error" : "좋아요를 누르지 않은 책입니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = UserBookLikeSerializer(book_like[0])
        return Response(serializer.data, status=status.HTTP_200_OK)