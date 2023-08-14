from Annotation.models import *
from Book.models import BookInfo
from User.models import User

from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status

# def assignAnnotationNum(book_id, user_id, page):
#     annotations = AnnotationInfo.objects.filter(book_id=book_id, user_id=user_id).order_by('annotation_num').all()
#     if len(annotations) == 0:
#         return 1
#     for i in len(annotations):
#         if annotations[i]<page and page<annotations[i+1]:
            
class AnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annotation
        fields = ['annotation_id', 'annotation']
        
class AnnotationCreateSerializer(serializers.ModelSerializer):
    annotation = serializers.CharField(write_only=True)
    page = serializers.IntegerField(write_only=True)
    class Meta:
        model = AnnotationInfo
        fields = ['annotation_id', 'page', 'annotation']
        
    def create(self, validated_data):
        user = User.object.get(id=self.context.get('user_id'))
        book = BookInfo.objects.get(book_id=self.context.get('book_id'))
        bookfile = self.context.get('book_page_file')
        
        if user is None:
            return Response({"error":"존재하지 않는 유저입니다."},status=status.HTTP_400_BAD_REQUEST)
        if book is None:
            return Response({"error":"존재하지 않는 책입니다."},status=status.HTTP_400_BAD_REQUEST)
        if bookfile is None:
            return Response({"error":"존재하지 않는 페이지입니다."},status=status.HTTP_400_BAD_REQUEST)
        
        annotation_info = AnnotationInfo.objects.create(
            book_id=book,
            user_id=user,
            file_id=bookfile,
            page=validated_data['page'],
        )
        annotation = Annotation.objects.create(
            annotation_id=annotation_info,
            annotation=validated_data['annotation'],
        )
        return annotation_info
    
class AnnotationEditSerializer(serializers.ModelSerializer):
    annotation = AnnotationSerializer()
    class Meta:
        model = AnnotationInfo
        fields = '__all__'