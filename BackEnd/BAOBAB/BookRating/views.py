from .api.serializers import BookRatingSerializer

from BookRating.models import BookRating
from Book.models import BookInfo

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class BookRatingView(APIView):
    serializer_class = BookRatingSerializer
    
    def post(self, request, *args, **kwargs):
        user_id = self.request.user
        book_id = kwargs.get('pk')
        
        book = BookInfo.objects.get(book_id=book_id)
        if book is None:
            return Response({"error":"존재하지 않는 책입니다."},status=status.HTTP_400_BAD_REQUEST)
        
        book_rating = BookRating.objects.filter(user_id=user_id, book_id=book_id)
        if book_rating.exists() :
            return Response({"error":"이미 평가한 책입니다."},status=status.HTTP_400_BAD_REQUEST)
        
        rating_count = BookRating.objects.filter(book_id=book_id).count()
        prev_rating = book.average_rating * rating_count
        book.average_rating = (prev_rating + float(request.data['rating'])) / (rating_count + 1)
        book.save()
        
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user_id=user_id, book_id=book)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, *args, **kwargs):
        user_id = self.request.user
        book_id = kwargs.get('pk')
        
        book = BookInfo.objects.get(book_id=book_id)
        if book is None:
            return Response({"error":"존재하지 않는 책입니다."},status=status.HTTP_400_BAD_REQUEST)
        
        book_rating = BookRating.objects.filter(user_id=user_id, book_id=book_id)
        if not book_rating.exists() :
            return Response({"error":"평가하지 않은 책입니다."},status=status.HTTP_400_BAD_REQUEST)
        
        rating_count = BookRating.objects.filter(book_id=book_id).count()
        prev_rating = book.average_rating * rating_count
        book.average_rating = (prev_rating - float(book_rating[0].rating)) / (rating_count - 1)
        book.save()
        
        book_rating.delete()
        return Response(data={"message": "성공적으로 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)
    
    def update(self, request, *args, **kwargs):
        user_id = self.request.user
        book_id = kwargs.get('pk')
        
        book = BookInfo.objects.get(book_id=book_id)
        if book is None:
            return Response({"error":"존재하지 않는 책입니다."},status=status.HTTP_400_BAD_REQUEST)
        
        book_rating = BookRating.objects.filter(user_id=user_id, book_id=book_id)
        if not book_rating.exists() :
            return Response({"error":"평가하지 않은 책입니다."},status=status.HTTP_400_BAD_REQUEST)
        
        rating_count = BookRating.objects.filter(book_id=book_id).count()
        prev_rating = book.average_rating * rating_count
        book.average_rating = (prev_rating - float(book_rating[0].rating) + float(request.data['rating'])) / (rating_count)
        book.save()
        
        serializer = self.serializer_class(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.update(book_rating[0], serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)