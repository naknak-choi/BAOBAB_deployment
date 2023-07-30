from django.urls import path
from . import views

urlpatterns = [
    path("uploadBook/", views.CreateBookView.as_view()),
    path("ratingBook/<int:pk>/", views.BookStatsAddView.as_view())
]
