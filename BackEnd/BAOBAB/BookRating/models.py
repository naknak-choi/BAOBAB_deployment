from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class BookRating(models.Model):
    rating_id = models.AutoField(primary_key=True)
    
    user_id = models.ForeignKey('User.User', on_delete=models.CASCADE)
    book_id = models.ForeignKey('Book.BookInfo', on_delete=models.CASCADE)
    
    rating = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        default=0.0
    )
    review = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f'{self.user_id}님의 {self.book_id} 책 평가'