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
    serializer_class = BookCreateSerializer
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