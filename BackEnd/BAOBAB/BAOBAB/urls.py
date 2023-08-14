from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    
    path("library/", include("Book.urls")),
    path("category/", include("Category.urls")),
    path('comment/', include('Comment.urls')),
    path('user/', include('User.urls')),
]
