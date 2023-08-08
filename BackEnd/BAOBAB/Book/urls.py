from django.urls import path
from .views import *

# staff_upload = views.BookStaffViewSet.as_view({
#     'get' : 'list',
#     'post' : 'create',
# })
# staff_edit = views.BookStaffViewSet.as_view({
#     'get' : 'retrieve',
#     'delete': 'destroy',
#     'put': 'update'
# })

# user_list = views.BookUserViewSet.as_view({
#     'get': 'list',
# })
# user_detail = views.BookUserViewSet.as_view({
#     'get': 'retrieve',
# })

urlpatterns = [
    # path("staff/upload/", staff_upload),
    # path("staff/edit/<int:pk>/", staff_edit),
    
    # path("list/", user_list),
    # path("detail/<int:pk>/", user_detail),
    path("staff/create/", BookStaffView.as_view()),
]
