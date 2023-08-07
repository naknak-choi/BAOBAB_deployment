from django.urls import path
from .api.views import CustomRegisterView, AuthAPIView

urlpatterns = [
    path('register/', CustomRegisterView.as_view(), name='register'),
    
    path('login/', AuthAPIView.as_view(), name='login'), # post
    path('logout/', AuthAPIView.as_view(), name='logout'), # delete
    path('auth/', AuthAPIView.as_view(), name='auth'), # get
]
