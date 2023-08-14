from django.urls import path
from . import views

urlpatterns = [
    path("like/<int:pk>/", views.UserBookLikeView.as_view()),
    path("like/<int:pk>/delete/", views.UserBookLikeView.as_view())
]
