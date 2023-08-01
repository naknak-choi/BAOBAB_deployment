from .api.serializers import *
from User.api.serializers import *

from rest_framework import generics
from rest_framework import viewsets

from rest_framework.permissions import IsAdminUser

from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import *

class BookStatsAddView(generics.UpdateAPIView):
    serializer_class = BookRatingSerializer
    
    def update(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        
        if serializer.is_valid():
            book_id = kwargs.get('pk')
            
            if not BookInfo.objects.filter(pk=book_id).exists():
                return Response(status=status.HTTP_404_NOT_FOUND)
            
            book_stats = BookStats.objects.get(book_id=book_id)
            
            rating_count = book_stats.rating_count
            average_rating = book_stats.average_rating
            new_rating = float(request.data.get('average_rating'))
            
            if new_rating is None or new_rating < 0 or new_rating > 5:
                return Response({"error":"Invalid rating"},status=status.HTTP_400_BAD_REQUEST)
            
            new_rating = round(new_rating, 1)
            rating_count += 1
            average_rating = (average_rating * (rating_count - 1) + new_rating) / rating_count
            
            BookStats.objects.filter(book_id=book_id).update(rating_count=rating_count, average_rating=average_rating)
            
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookStaffViewSet(viewsets.ModelViewSet):
    queryset = BookInfo.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = BookStaffSerializer
    parser_classes = [MultiPartParser, FileUploadParser]
    
class BookUserViewSet(viewsets.ModelViewSet):
    queryset = BookInfo.objects.all()
    serializer_class = BookUserSerializer
