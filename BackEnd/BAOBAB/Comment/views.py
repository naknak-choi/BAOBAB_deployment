from .api.serializers import CommentSerializer, CommentInfoSerializer
from .models import Comment, CommentInfo

from Book.models import BookInfo, BookFile

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class CommentCreateView(APIView):
    serializer_class = CommentInfoSerializer
    
    def post(self, request, *args, **kwargs):
        book_id = kwargs['book_id']
        user_id = request.user
        
        book = BookInfo.objects.filter(book_id=book_id).first()
        if not book:
            return Response({"message": "책이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        if request.data.get('parentComment_id'):
            parentComment = request.data.get('parentComment_id')
        else :
            parentComment = None
        
        if request.data.get('page'):
            file_id = BookFile.objects.filter(book_id=book, page=request.data.get('page')).first()
        else :
            file_id = None
            
        comment_info = CommentInfo.objects.create(
            user_id = user_id,
            book_id = book,
            file_id = file_id,
            parentComment_id = parentComment,
            created_at = request.data.get('created_at'),
            liked = request.data.get('liked'),
        )
        
        comment = Comment.objects.create(
            comment = request.data.get('comment'),
            comment_id = comment_info,
        )
        
        return Response({"message": "댓글 작성 성공"}, status=status.HTTP_201_CREATED)
    
class CommetEditView(APIView):
    serializer_class = CommentInfoSerializer
    
    def put(self, request, *args, **kwargs):
        comment_id = kwargs['comment_id']
        user_id = request.user
        
        comment_info = CommentInfo.objects.filter(comment_id=comment_id).first()
        
        if comment_info.user_id != user_id:
            return Response({"message": "댓글 작성자가 아닙니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not comment_info:
            return Response({"message": "댓글이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        if comment_info.user_id != user_id:
            return Response({"message": "댓글 작성자가 아닙니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        comment = Comment.objects.filter(comment_id=comment_id).first()
        if not comment:
            return Response({"message": "댓글이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        comment.comment = request.data.get('comment')
        comment.save()
        
        return Response({"message": "댓글 수정 성공"}, status=status.HTTP_200_OK)
    
    def delete(self, request, *args, **kwargs):
        comment_id = kwargs['comment_id']
        user_id = request.user
        comment_info = CommentInfo.objects.filter(comment_id=comment_id).first()
        
        if comment_info.user_id != user_id:
            return Response({"message": "댓글 작성자가 아닙니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not comment_info:
            return Response({"message": "댓글이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        if comment_info.user_id != user_id:
            return Response({"message": "댓글 작성자가 아닙니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        comment = Comment.objects.filter(comment_id=comment_id).first()
        if not comment:
            return Response({"message": "댓글이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        comment.delete()
        comment_info.delete()
        
        return Response({"message": "댓글 삭제 성공"}, status=status.HTTP_200_OK)