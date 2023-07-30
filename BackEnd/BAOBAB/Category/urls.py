from django.urls import path
from . import views

urlpatterns=[
    path("create/", views.CreateCategoryView.as_view()),
]