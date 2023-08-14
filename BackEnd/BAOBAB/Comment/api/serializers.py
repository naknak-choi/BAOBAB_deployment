from ..models import Comment, CommentInfo
from rest_framework import serializers

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        
class CommentInfoSerializer(serializers.ModelSerializer):
    comment = serializers.CharField(write_only=True)
    
    comment_text = CommentSerializer(read_only=True)
    class Meta:
        model = CommentInfo
        fields = [
            'comment_id',
            'user_id',
            'book_id',
            'file_id',
            'parentComment_id',
            'comment',
            'comment_text',
        ]