from django.urls import path
from .views import *
from . import views

user_detail = views.UserViewSets.as_view({
    'get': 'retrieve',
})

urlpatterns = [
    path('detail/<int:id>', user_detail, name='user_detail'),
]
