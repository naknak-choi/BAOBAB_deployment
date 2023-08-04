from django.urls import path
from .views import *
from . import views

user_detail = views.UserViewSets.as_view({
    'get': 'retrieve',
})

urlpatterns = [
    path('register', RegistrationAPIView.as_view()),
    path('login', LoginAPIView.as_view()),
    path('current', UserRetrieveUpdateAPIView.as_view()),
    path('detail/<int:id>', user_detail, name='user_detail'),
]
