from django.contrib import admin
from django.urls import path, include

# from dj_rest_auth.registration.views import RegisterView

# from User.api.views import RegisterView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("library/", include("Book.urls")),
    path("category/", include("Category.urls")),
    path("user_like/", include("UserBookLike.urls")),
    path('annotation/', include('Annotation.urls')),
    path('comment/', include('Comment.urls')),
    
    path('user/', include('User.urls')),
    
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    # path('dj-rest-auth/registration/', RegisterView.as_view(), name='account_register'),
]
