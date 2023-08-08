from django.urls import path
from .api.views import *


urlpatterns = [
    path('register/', CustomRegisterView.as_view(), name='register'),
    
    path('login/', LoginView.as_view(), name='login'), # post
    path('logout/', LogoutView.as_view(), name='logout'), # delete
    
    path('mypage/', MypageView.as_view(), name='auth'), # get
    path('mypage/update/', UserUpdateView.as_view(), name='update'), # put
    path('mypage/delete/', UserDeleteView.as_view(), name='delete'), # delete
    path('mypage/password/change/', UserPasswordChangeView.as_view(), name='password_change'), # post
    path('password/reset/', UserPasswordResetView.as_view(), name='password_reset'), # post
    
    # refresh token을 body에 넣어서 post
    # 새로운 access token을 받아옴
    path("auth/refresh/", CookieTokenObtainPairView.as_view()),
]
