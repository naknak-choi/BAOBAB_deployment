from django.db import models

# Create your models here.

class AnnotationInfo(models.Model):
    annotation_id = models.AutoField(primary_key=True)
    
    user_id = models.ForeignKey('User.User', on_delete=models.CASCADE, related_name='user_annotation')
    book_id = models.ForeignKey('Book.BookInfo', on_delete=models.CASCADE, related_name='book_annotation')
    file_id = models.ForeignKey('Book.BookFile', on_delete=models.CASCADE, related_name='file_annotation')
    
    annotation_num = models.IntegerField(default=1)
    
    page = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
class Annotation(models.Model):
    annotation_id = models.OneToOneField(AnnotationInfo, on_delete=models.CASCADE, related_name='annotation')
    annotation = models.TextField()
    
    def __str__(self):
        return str(self.annotation_id) + ' ' + self.annotation