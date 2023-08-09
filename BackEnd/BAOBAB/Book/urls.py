from django.urls import path
from .views import *

user_list_view = BookUserView.as_view({
    'get': 'list',
})

user_detail_view = BookUserView.as_view({
    'get': 'retrieve',
})

urlpatterns = [
    path("staff/create/", BookStaffView.as_view()),
    path("staff/delete/", BookStaffView.as_view()),
    
    path('', user_list_view, name='user-list'),
    path('detail/<int:pk>/', user_detail_view, name='user-detail'),
]
