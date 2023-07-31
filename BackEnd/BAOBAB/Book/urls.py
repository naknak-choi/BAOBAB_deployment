from django.urls import path
from . import views

urlpatterns = [
    path("uploadBook/", views.CreateBookView.as_view()),
    path("ratingBook/<int:pk>/", views.BookStatsAddView.as_view()),
    path("listup/", views.BookInfoView.as_view()),
    path("detail/<int:pk>/", views.BookInfoView.as_view()),
    path("update/<int:pk>/", views.BookUpdateView.as_view()),
]
