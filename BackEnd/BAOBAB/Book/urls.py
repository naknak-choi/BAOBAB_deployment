from django.urls import path
from . import views

urlpatterns = [
    # path("upload/", views.CreateBookInfoView.as_view()),
    path("uploadBook/", views.CreateBookView.as_view()),
]
