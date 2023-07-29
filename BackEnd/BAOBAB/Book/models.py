from django.db import models

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
    book_id = models.AutoField(primary_key=True)
    mainCategory = models.OneToOneField(
        Category, 
        on_delete=models.SET_DEFAULT, 
        related_name='mainCategory',
        blank=True,
        default=default_category(),
        validators=[main_category_validator],
    )
    subCategory = models.OneToOneField(
        Category,
        on_delete=models.SET_DEFAULT,
        related_name='subCategory',
        blank=True,
        default=default_category(),
        validators=[sub_category_validator],
    )

    book_Name = models.CharField(max_length=255)
    author = models.CharField(max_length=20)
    is_popular = models.BooleanField(default=False)
    publication_year = models.CharField(max_length=20)
    publication_month = models.CharField(max_length=10)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.book_Name
    
    def clean(self):
        if self.subCategory and self.mainCategory:
            if self.subCategory.mainCategory_name != self.mainCategory:
                raise ValidationError("선택한 중분류는 해당 대분류에 속하지 않습니다.")


class BookFile(models.Model):
    book_id = models.OneToOneField(BookInfo, on_delete=models.CASCADE)
    book_file = models.FileField()


class BookCover(models.Model):
    book_id = models.OneToOneField(BookInfo, on_delete=models.CASCADE)
    book_cover = models.ImageField()


class BookStats(models.Model):
    book_id = models.OneToOneField(BookInfo, on_delete=models.CASCADE)
    
    rating = models.FloatField(default=0.0)
    liked = models.IntegerField(default=0)
    views = models.IntegerField(default=0)