from django.urls import path
from . import views

category_create = views.CategoryViewSet.as_view({
    'post': 'create',
})

category_edit = views.CategoryViewSet.as_view({
    'get': 'retrieve',
    'delete': 'destroy',
    'put': 'update',
})

urlpatterns=[
    path("create/", category_create),
    path("edit/<str:pk>/", category_edit)
]