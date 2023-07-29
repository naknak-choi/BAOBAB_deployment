from django.apps import AppConfig
from django.db.models.signals import post_migrate

def add_default_category(sender, **kwargs):
    from .models import Category
    if not Category.objects.filter(category_name='미분류').exists():
        category = Category.objects.create(category_name='미분류')
        category.mainCategory_name = category
        category.is_main = True
        category.save()

class CategoryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "Category"
    
    def ready(self):
        post_migrate.connect(add_default_category, sender=self)