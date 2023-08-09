from .views import *
from BookRating.views import BookRatingView

from django.urls import path

user_list_view = BookUserView.as_view({
    'get': 'list',
    'put': 'update',
    'delete': 'destroy',
})

user_detail_view = BookUserView.as_view({
    'get': 'retrieve',
})

urlpatterns = [
    path("staff/create/", BookStaffView.as_view()),
    path("staff/delete/<int:pk>/", BookStaffView.as_view()),
    path('staff/<int:pk>/update/', user_list_view, name='user-update'),
    
    path('', user_list_view, name='user-list'),
    path('detail/<int:pk>/', user_detail_view, name='user-detail'),
    
    path('detail/<int:pk>/rating/', BookRatingView.as_view(), name='user-rating'),
    path('detail/<int:pk>/rating/update/', BookRatingView.as_view(), name='user-rating'),
    path('detail/<int:pk>/rating/delete/', BookRatingView.as_view(), name='user-rating'),
]
