from django.db import models

# Create your models here.

class Bookmark(models.Model):
    bookmark_id = models.AutoField(primary_key=True)
    
    user_id = models.ForeignKey('User.User', on_delete=models.CASCADE)
    book_id = models.ForeignKey('Book.BookInfo', on_delete=models.CASCADE)
    file_id = models.ForeignKey('Book.BookFile', on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.book_id.book_name + " " + str(self.file_id.page) + " " + str(self.created_at)