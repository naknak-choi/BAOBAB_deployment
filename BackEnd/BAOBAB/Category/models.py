from django.db import models

class Category(models.Model):
    category_id = models.AutoField(primary_key=True, default=' ')
    category_name = models.CharField(max_length=255, unique=True)
    mainCategory_name = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    is_main = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.category_name