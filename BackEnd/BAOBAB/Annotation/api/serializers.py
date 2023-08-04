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

class AnnotationSerializer(serializers.ModelSerializer):
    annotation = serializers.CharField()
    
    annotation_text = AnnotationSerializer(source='annotation', read_only=True)
    class Meta:
        model = AnnotationInfo
        fields = ['annotation_id', 'page', 'annotation', 'annotation_text']
        # fields = ['annotation_id', 'page', 'annotation_text']
        
    def create(self, validated_data):
        user = User.object.get(id=self.context.get('user_id'))
        book = BookInfo.objects.get(book_id=self.context.get('book_id'))
        
        if user is None:
            return Response({"error":"존재하지 않는 유저입니다."},status=status.HTTP_400_BAD_REQUEST)
        if book is None:
            return Response({"error":"존재하지 않는 책입니다."},status=status.HTTP_400_BAD_REQUEST)
        
        annotation_info = AnnotationInfo.objects.create(
            book_id=book,
            user_id=user,
            page=validated_data['page'],
        )
        annotation = Annotation.objects.create(
            annotation_id=annotation_info,
            annotation=validated_data['annotation'],
        )
        
        return annotation_info