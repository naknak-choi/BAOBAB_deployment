from .api.serializers import *
from .models import *
from Book.models import BookInfo
from User.models import User

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

class AnnotationCreateView(APIView):
    serializer_class = AnnotationSerializer
    
    def post(self, request, *args, **kwargs):
        user_id = self.request.user.id
        book_id = kwargs.get('book_id')
        print(user_id, book_id)
        book = BookInfo.objects.get(book_id=book_id)
        if book is None:
            return Response({"error":"존재하지 않는 책입니다."},status=status.HTTP_400_BAD_REQUEST)
        
        user = User.object.get(id=user_id)
        if user is None:
            return Response({"error":"존재하지 않는 유저입니다."},status=status.HTTP_400_BAD_REQUEST)

        context = {
            'user_id': user_id,
            'book_id': book_id
        }
        
        serializer = self.serializer_class(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else :
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class AnnotationListView(APIView):
    serializer_class = AnnotationSerializer
    
    def get(self, request, *args, **kwargs):
        user_id = self.request.user.id
        book_id = kwargs.get('book_id')
        list_id = kwargs.get('list_id')
        
        if list_id is None:
            annotation_list = AnnotationInfo.objects.filter(user_id=user_id, book_id=book_id)
            return Response(AnnotationSerializer(annotation_list, many=True).data, status=status.HTTP_200_OK)
        else:
            return self.retrieve(request, *args, **kwargs)
        
    def delete(self, request, *args, **kwargs):
        user_id = self.request.user.id
        book_id = kwargs.get('book_id')
        list_id = kwargs.get('list_id')
        
        annotation = AnnotationInfo.objects.get(user_id=user_id, book_id=book_id, annotation_id=list_id)
        if annotation is None:
            return Response({"error":"존재하지 않는 어노테이션입니다."},status=status.HTTP_400_BAD_REQUEST)
        annotation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def retrieve(self, request, *args, **kwargs):
        user_id = self.request.user.id
        book_id = kwargs.get('book_id')
        list_id = kwargs.get('list_id')
        
        annotation = AnnotationInfo.objects.get(user_id=user_id, book_id=book_id, annotation_id=list_id)
        return Response(AnnotationSerializer(annotation).data, status=status.HTTP_200_OK)