from .views import *
from Annotation.views import AnnotationCreateView, AnnotationListView
from BookRating.views import BookRatingView
from Bookmark.views import BookmarkView
from UserBookLike.views import UserBookLikeView
from Comment.views import CommentCreateView, CommetEditView

from django.urls import path

user_list_view = BookUserView.as_view({
    'get': 'list',
})

user_detail_view = BookUserView.as_view({
    'get': 'retrieve',
})

urlpatterns = [
    path("staff/create/", BookStaffView.as_view()),
    path("staff/delete/<int:book_id>/", BookStaffView.as_view()),
    path('staff/update/<int:book_id>/', BookStaffView.as_view(), name='user-update'),
    
    path('', user_list_view, name='user-list'),
    path('detail/<int:pk>/', user_detail_view, name='user-detail'),
    path('detail/<int:book_id>/page/', BookPageListView.as_view(), name='user-page'),
    
    path('detail/<int:book_id>/bookmark/', BookmarkView.as_view(), name='user-bookmark'),
    
    path('detail/<int:book_id>/userbooklike/', UserBookLikeView.as_view(), name='user-booklike'),
    
    path('detail/<int:book_id>/comment/create/', CommentCreateView.as_view(), name='user-comment'),
    path('detail/<int:book_id>/comment/list/', BookCommentListView.as_view(), name='user-comment'),
    path('detail/<int:book_id>/comment/<int:comment_id>/', CommetEditView.as_view(), name='user-comment'),
    
    path('detail/<int:book_id>/annotation/create/', AnnotationCreateView.as_view(), name='user-annotation'),
    path('detail/<int:book_id>/annotation/<int:annotation_id>/', AnnotationListView.as_view(), name='user-annotation'),

    path('detail/<int:book_id>/rating/create/', BookRatingView.as_view(), name='user-rating'),
    path('detail/<int:book_id>/rating/update/', BookRatingView.as_view(), name='user-rating'),
    path('detail/<int:book_id>/rating/delete/', BookRatingView.as_view(), name='user-rating'),
]
