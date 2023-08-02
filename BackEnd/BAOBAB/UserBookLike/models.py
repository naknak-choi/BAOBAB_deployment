from django.db import models

# Create your models here.

class UserBookLike(models.Model):
    list_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('User.User', on_delete=models.CASCADE)
    book_id = models.ForeignKey('Book.BookInfo', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user_id.username + ' ' + self.book_id.book_Name