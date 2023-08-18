from ..models import Comment, CommentInfo
from rest_framework import serializers

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        
class CommentInfoSerializer(serializers.ModelSerializer):
    comment = serializers.CharField(write_only=True)
    comment_text = CommentSerializer(source='comment', read_only=True)
    
    user_name = serializers.CharField(source='user_id.nickname', read_only=True)

    class Meta:
        model = CommentInfo
        fields = [
            'comment_id',
            'user_id',
            'user_name',
            'book_id',
            'file_id',
            'parentComment_id',
            'comment',
            'comment_text',
            'created_at',
            'liked'
        ]