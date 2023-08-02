from .api.serializers import *
from Book.models import *

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class UserBookLikeView(APIView):
    serializer_class = UserBookLikePostSerializer
        
    def post(self, request, *args, **kwargs):
        user_id = self.request.user
        book_id = kwargs.get('pk')
        context = {
            'user': user_id,
            'book_id': book_id
        }
        serializer = self.serializer_class(data=request.data, context=context)
        
        book = BookInfo.objects.get(book_id=book_id)
        if book is None:
            return Response({"error":"존재하지 않는 책입니다."},status=status.HTTP_400_BAD_REQUEST)
        book_like = UserBookLike.objects.filter(user_id=user_id, book_id=book_id)
        if book_like.exists():
            return Response({"error" : "이미 좋아요를 누른 책입니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)