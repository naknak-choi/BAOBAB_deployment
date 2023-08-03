from django.urls import path
from . import views

# test = views.TestViewSet.as_view({
#     'post': 'create'
# })

urlpatterns = [
    path("like/<int:pk>", views.UserBookLikeView.as_view()),
    path("like/<int:pk>/delete", views.UserBookLikeDeleteView.as_view())
]
