from django.urls import path
from .api.views import RegisterView, MypageView, LoginView, LogoutView, UserUpdateView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    
    path('login/', LoginView.as_view(), name='login'), # post
    path('logout/', LogoutView.as_view(), name='logout'), # delete
    path('mypage/', MypageView.as_view(), name='auth'), # get
    path('mypage/update/', UserUpdateView.as_view(), name='update'), # put
]
