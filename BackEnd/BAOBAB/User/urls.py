from django.urls import path
from .api.views import CustomRegisterView

urlpatterns = [
    path('register/', CustomRegisterView.as_view(), name='register')
]
