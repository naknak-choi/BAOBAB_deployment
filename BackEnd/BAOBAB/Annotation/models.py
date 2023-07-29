from django.db import models

# Create your models here.

class AnnotationInfo(models.Model):
    annotation_id = models.AutoField(primary_key=True)
    
    user_id = models.ForeignKey('User.User', on_delete=models.CASCADE)
    book_id = models.ForeignKey('Book.BookInfo', on_delete=models.CASCADE)
    
    annotation_num = models.IntegerField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    
class Annotation(models.Model):
    annotation_id = models.OneToOneField(AnnotationInfo, on_delete=models.CASCADE)
    annotation = models.TextField()