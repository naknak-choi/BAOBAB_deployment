from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("library/", include("Book.urls")),
    path("category/", include("Category.urls")),
    path("user_like/", include("UserBookLike.urls")),
]
