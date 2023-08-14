from django.urls import path
from .views import *
from . import views

# annotation_craete = views.AnnotationViewSet.as_view({
#     'post': 'create'
# })

urlpatterns = [
    path('create/<int:book_id>/', AnnotationCreateView.as_view(), name='annotation_create'),
    path('list/<int:book_id>/', AnnotationListView.as_view(), name='annotation_list'),
    path('list/<int:book_id>/<int:annotation_id>/', AnnotationListView.as_view(), name='annotation_list'),
]
