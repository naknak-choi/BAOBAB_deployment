from django.urls import path
from .views import *

urlpatterns = [
    path('register/', CustomRegisterView.as_view(), name='register'),
    
    path('verify_email/token=<str:token>', VerifyEmailView.as_view(), name='verify_email'),
    
    path('login/', LoginView.as_view(), name='login'), # post
    path('logout/', LogoutView.as_view(), name='logout'), # delete
    
    path('mypage/', MypageView.as_view(), name='auth'), # get
    path('mypage/update/', UserUpdateView.as_view(), name='update'), # put
    path('mypage/delete/', UserDeleteView.as_view(), name='delete'), # delete
    
    path('mypage/like/', UserBookLikeView.as_view(), name='like'), # get
    path('mypage/annotation/', UserAnnotationView.as_view(), name='annotation'), # get
    path('mypage/comment/', UserCommentView.as_view(), name='comment'), # get
    path('mypage/bookmark/', UserBookmarkView.as_view(), name='bookmark'), # get
    
    path('mypage/password/change/', UserPasswordChangeView.as_view(), name='password_change'), # post
    path('password/reset/', UserPasswordResetView.as_view(), name='password_reset'), # post
    
    # refresh token을 body에 넣어서 post
    # 새로운 access, refresh token을 받아옴
    path("auth/refresh/", CookieTokenObtainPairView.as_view()),
]
