from .api.serializers import *

from rest_framework.permissions import IsAdminUser
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

# class CreateBookInfoView(generics.CreateAPIView):
#     serializer_class = BookInfoSerializer
#     permission_classes = [IsAdminUser]
    
#     def create(self, request, *args, **kwargs):
#         data = request.data
#         book_info_serializers = self.get_serializer(data=data)
        
#         if book_info_serializers.is_valid():
#             book_info_serializers.save()
#         else:
#             return Response(book_info_serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        
class CreateBookView(generics.CreateAPIView):
    serializer_class = CreateBookSerializer
    permission_classes = [IsAdminUser]
    
    def create(self, request, *args, **kwargs):
        data = request.data
        book_serializer = self.get_serializer(data=data)
        
        if book_serializer.is_valid():
            book = book_serializer.save()
            
            return Response(book_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(book_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        #     book_file_serializer = BookInfoSerializer(data=data.get('BookFile'))
        #     book_cover_serializer = BookInfoSerializer(data=data.get('BookCover'))
            
        #     if book_file_serializer.is_valid() and book_cover_serializer.is_valid():
        #         book_file_serializer.save(book = book)
        #         book_cover_serializer.save(book = book)
        #     else:
        #         errors = {}
        #         errors.update(book_file_serializer.errors)
        #         errors.update(book_cover_serializer.errors)
        #         return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        # else:
        #     return Response(book_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class BookStatsAddView(generics.UpdateAPIView):
    serializer_class = BookRatingSerializer
    
    def update(self, request, *args, **kwargs):
        data = request.data
        serializers = self.get_serializer(data=data)
        
        if serializers.is_valid():
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
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # def update(self, request, *args, **kwargs):
    #     serializers = self.get_serializer(data=request.data)
    #     if not serializers.is_valid():
    #         return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        
    #     elif not BookInfo.objects.filter(pk=kwargs.get('pk')).exists():
    #         return Response(status=status.HTTP_404_NOT_FOUND)
        
    #     book_id = kwargs.get('pk')
    #     book_stats = BookStats.objects.get(book_id=book_id)
        
    #     rating_count = book_stats.rating_count
    #     rating_count += 1
        
    #     average_rating = book_stats.average_rating
    #     new_rating = request.data.get('average_rating')
    #     average_rating = average_rating / rating_count
        
    #     BookStats.objects.filter(book_id=book_id).update(rating_count=rating_count, average_rating=average_rating)
        
    #     return Response(status=status.HTTP_200_OK)