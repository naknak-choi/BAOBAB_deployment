from django.db import models

# Create your models here.

class CommentInfo(models.Model):
    comment_id = models.AutoField(primary_key=True)
    
    user_id = models.ForeignKey('User.User', on_delete=models.CASCADE)
    book_id = models.ForeignKey('Book.BookInfo', on_delete=models.CASCADE)
    parentComment_id = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    
    liked = models.PositiveSmallIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
class Comment(models.Model):
    comment_id = models.OneToOneField(CommentInfo, on_delete=models.CASCADE)
    comment = models.TextField()
    
    def __str__(self):
        return self.comment