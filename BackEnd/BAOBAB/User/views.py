from .api.serializers import UserRegisterSerializer, UserSerializer
from .utils import *
from User.models import User

from UserBookLike.models import UserBookLike
from UserBookLike.api.serializers import UserBookLikeSerializer

from Annotation.models import AnnotationInfo
from Annotation.api.serializers import AnnotationEditSerializer

from Book.models import BookInfo

from Bookmark.models import Bookmark
from Bookmark.api.serializers import BookmarkSerializer

from BookRating.models import BookRating
from BookRating.api.serializers import BookRatingSerializer

from Comment.models import CommentInfo
from Comment.api.serializers import CommentInfoSerializer

from BAOBAB.settings import SECRET_KEY

from dj_rest_auth.registration.views import RegisterView

from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail

from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

import jwt
import time

class CustomRegisterView(RegisterView):
    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save(request)
            user.is_active = False
            token = TokenObtainPairSerializer.get_token(user)
            access_token = str(token.access_token)
            refresh_token = str(token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "register successs",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            
            user.save()
            send_verification_email(user)
            
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    def post(self, request):
        # 유저 인증
        user = authenticate(
            email=request.data.get("email"),
            password=request.data.get("password"),
        )
        
        user.last_login = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        user.save()

        # 이미 회원가입 된 유저일 때
        if user is not None:
            serializer = UserSerializer(user)
            # jwt 토큰 접근
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "login success",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            # jwt 토큰 => 쿠키에 저장
            res.set_cookie("access", access_token, httponly=True, max_age=300)
            res.set_cookie("refresh", refresh_token, httponly=True, max_age=300)
            return res
        else:
            return Response({'error' : '존재하지 않는 회원정보입니다.'}, status=status.HTTP_400_BAD_REQUEST)
class MypageView(APIView):
    # 유저 정보 확인
    def get(self, request):
        try:
            user = request.user
            serializer = UserSerializer(user)
            return Response(serializer.data)    
        except(jwt.exceptions.ExpiredSignatureError):
            return Response(status=status.HTTP_401_UNAUTHORIZED) 
class LogoutView(APIView):
    # 로그아웃
    def delete(self, request):
        # 쿠키에 저장된 토큰 삭제 => 로그아웃 처리
        response = Response({
            "message": "Logout success"
            }, status=status.HTTP_202_ACCEPTED)
        response.delete_cookie("access")
        response.delete_cookie("refresh")
        return response

class UserUpdateView(APIView):
    def put(self, request):
        user = request.user
        re_ninkname = request.data.get('nickname')
        other_user = User.objects.filter(nickname = re_ninkname).first()
        if other_user is not None:
            return Response({'error' : '이미 존재하는 닉네임입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        user.nickname = re_ninkname
        user.save()
        return Response({'detail' : '성공적으로 수정되었습니다.'}, status=status.HTTP_200_OK)
    
class CookieTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = TokenObtainPairSerializer(data=request.data)
        if serializer.is_valid():
            access_token = serializer.validated_data.get('access')
            refresh_token = serializer.validated_data.get('refresh')
            response = Response({
                "access": access_token,
                "refresh": refresh_token,
                }, status=status.HTTP_200_OK)
            response.set_cookie('access', access_token)
            response.set_cookie('refresh', refresh_token)
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserDeleteView(APIView):
    def delete(self, request):
        user = request.user
        user.delete()
        return Response({"detail" : "성공적으로 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)
    
class UserPasswordChangeView(APIView):
    def post(self, request):
        user = request.user
        password1 = request.data.get('password1')
        password2 = request.data.get('password2')
        if password1 != password2:
            return Response({'error' : '비밀번호가 일치하지 않습니다.'},status=status.HTTP_400_BAD_REQUEST)
        user.set_password(password1)
        user.save()
        return Response({'detail' : '비밀번호가 변경되었습니다.'}, status=status.HTTP_200_OK)
    
class UserPasswordResetView(APIView):
    def post(self, request):
        email = request.data.get('email')
        user = get_object_or_404(User, email=email)
        new_password = User.objects.make_random_password()
        
        subject = '[BAOBAB] 임시 비밀번호 발급 안내'
        message = '임시 비밀번호 로그인 후 비밀번호를 변경해주세요. \n 임시 비밀번호 : ' + new_password
        from_email = settings.EMAIL_HOST_USER
        respone = {
            'temp_password': '임시비밀번호가 발급되었습니다.'
        }
        send_mail(subject, message, from_email, [email], fail_silently=False)
        user.set_password(new_password)
        user.save()
        return Response(respone, status=status.HTTP_200_OK)
    
class UserBookLikeView(APIView):
    def get(self, request):
        user = request.user
        book_like = UserBookLike.objects.filter(user_id=user)
        serializer = UserBookLikeSerializer(book_like, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserAnnotationView(APIView):
    def get(self, request):
        user = request.user
        annotation = AnnotationInfo.objects.filter(user_id=user)
        serializer = AnnotationEditSerializer(annotation, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class UserCommentView(APIView):
    def get(self, request):
        user = request.user
        comment = CommentInfo.objects.filter(user_id=user)
        serializer = CommentInfoSerializer(comment, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class UserBookRatingView(APIView):
    def get(self, request):
        user = request.user
        book_rating = BookRating.objects.filter(user_id=user)
        serializer = BookRatingSerializer(book_rating, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserBookmarkView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        bookmark = Bookmark.objects.filter(user_id=user)
        serializer = BookmarkSerializer(bookmark, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class VerifyEmailView(APIView):
    def get(self, request, *args, **kwargs):
        print(self.kwargs['token'])
        token = self.kwargs['token']
        decoded_user_id, decoded_email, decoded_timestamp = verify_email_token(token)
        if decoded_timestamp + 60*60 < time.time():
            return Response({'detail' : '이메일 인증 시간이 만료되었습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(pk=decoded_user_id)
        if user.email == decoded_email:
            user.is_active = True
            user.save()
            return Response({'detail' : '이메일 인증이 완료되었습니다.'}, status=status.HTTP_200_OK)