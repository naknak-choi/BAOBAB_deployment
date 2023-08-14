from django.contrib import admin

from .models import *

admin.site.register(BookInfo)
admin.site.register(BookCover)
admin.site.register(BookFile)