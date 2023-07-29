from django.db import models

class Category(models.Model):
    category_name = models.CharField(max_length=255, primary_key=True, unique=True)
    mainCategory_name = models.OneToOneField('self', on_delete=models.CASCADE, unique=True, null=True, blank=True)
    is_main = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.category_name