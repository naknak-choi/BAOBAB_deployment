from .serializers import UserRegisterSerializer, UserSerializer
from BAOBAB.settings import SECRET_KEY
from User.models import User

from dj_rest_auth.registration.views import RegisterView

from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

import jwt

class CustomRegisterView(RegisterView):
    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save(request)
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
            
            # jwt 토큰 => 쿠키에 저장
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class LoginView(APIView):
    def post(self, request):
        # 유저 인증
        user = authenticate(
            email=request.data.get("email"), password=request.data.get("password")
        )
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
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            return res
        else:
            return Response({'error' : '존재하지 않는 회원정보입니다.'}, status=status.HTTP_400_BAD_REQUEST)
class MypageView(APIView):
    # 유저 정보 확인
    def get(self, request):
        try:
            # access token을 decode 해서 유저 id 추출 => 유저 식별
            access = request.COOKIES['access']
            payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk=pk)
            serializer = UserSerializer(instance=user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except(jwt.exceptions.ExpiredSignatureError):
            return Response(status=status.HTTP_401_UNAUTHORIZED) 
            # 토큰 만료 시 토큰 갱신
            # data = {'refresh': request.COOKIES.get('refresh', None)}
            # serializer = TokenRefreshSerializer(data=data)
            # if serializer.is_valid(raise_exception=True):
            #     access = serializer.data.get('access', None)
            #     refresh = serializer.data.get('refresh', None)
            #     payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
            #     pk = payload.get('user_id')
            #     user = get_object_or_404(User, pk=pk)
            #     serializer = UserSerializer(instance=user)
            #     res = Response(serializer.data, status=status.HTTP_200_OK)
            #     res.set_cookie('access', access)
            #     res.set_cookie('refresh', refresh)
            #     return res
            # raise jwt.exceptions.InvalidTokenError

        except(jwt.exceptions.InvalidTokenError):
            # 사용 불가능한 토큰일 때
            return Response(status=status.HTTP_400_BAD_REQUEST)
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
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

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
        return Response(status=status.HTTP_204_NO_CONTENT)
    
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
        new_password = User.object.make_random_password()
        respone = {
            'temp_password': new_password
        }
        user.set_password(new_password)
        user.save()
        return Response(respone, status=status.HTTP_200_OK)