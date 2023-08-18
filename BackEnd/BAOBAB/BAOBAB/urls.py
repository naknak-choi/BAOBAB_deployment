from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.urls import re_path


urlpatterns = [
    path("admin/", admin.site.urls),
    
    path("library/", include("Book.urls")),
    path("category/", include("Category.urls")),
    path('comment/', include('Comment.urls')),
    path('user/', include('User.urls')),
    re_path(r'^.*', TemplateView.as_view(template_name='index.html')),
    
]


