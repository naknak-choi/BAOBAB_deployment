from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

from Category.models import Category


def default_category():
    default = Category.objects.get(category_name='미분류')
    return default.pk

def main_category_validator(value):
    category = Category.objects.get(category_name=value)
    if not category.is_main:
        raise ValidationError("메인 카테고리만 선택할 수 있습니다.")

def sub_category_validator(value):
    category = Category.objects.get(category_name=value)
    if category.is_main:
        raise ValidationError("서브 카테고리만 선택할 수 있습니다.")

class BookInfo(models.Model):
    BOOK_CHOICES = [
        ('기증도서', '기증도서'),
        ('저작권 만료도서', '저작권 만료도서'),
    ]
    
    book_id = models.AutoField(primary_key=True)
    mainCategory = models.ForeignKey(
        Category, 
        on_delete=models.SET_DEFAULT,
        related_name='mainCategory',
        blank=True,
        default=default_category(),
        validators=[main_category_validator],
    )
    subCategory = models.ForeignKey(
        Category,
        on_delete=models.SET_DEFAULT,
        related_name='subCategory',
        blank=True,
        default=default_category(),
        validators=[sub_category_validator],
    )

    book_name = models.CharField(max_length=255)
    author = models.CharField(max_length=20)
    is_popular = models.BooleanField(default=False)
    publication_year = models.CharField(max_length=20)
    book_status = models.CharField(
        max_length=20,
        choices=BOOK_CHOICES,
        verbose_name='기증 / 만료 여부',
        default='기증도서',
        )
    
    views = models.PositiveIntegerField(default=0)
    like = models.PositiveIntegerField(default=0)
    average_rating = models.FloatField(default=0.0)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.book_name
    
    def clean(self):
        if self.subCategory and self.mainCategory:
            if self.subCategory.mainCategory_name != self.mainCategory:
                raise ValidationError("선택한 중분류는 해당 대분류에 속하지 않습니다.")

def upload_book_page_path(instance, filename):
    return f'media/{instance.book_id.book_name}/pages/{timezone.now().strftime("%Y%m%d_%H%M%S")}_{filename}'

def upload_book_cover_path(instance, filename):
    return f'media/{instance.book_id.book_name}/cover/{timezone.now().strftime("%Y%m%d_%H%M%S")}_{filename}'

class BookFile(models.Model):
    file_id = models.AutoField(primary_key=True)
    
    book_id = models.ForeignKey(BookInfo, on_delete=models.CASCADE)
    page_image = models.ImageField(upload_to=upload_book_page_path)
    page_num = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.book_id.book_name + " : " + str(self.page_num) + "Page"


class BookCover(models.Model):
    book_id = models.OneToOneField(BookInfo, on_delete=models.CASCADE)
    book_cover = models.ImageField(upload_to=upload_book_cover_path)
    
    def __str__(self):
        return self.book_id.book_name + "Cover"