from dj_rest_auth.registration.views import RegisterView
from .serializers import CustomRegisterSerializer
class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer

    def post(self, request, *args, **kwargs):
        # 여기에 추가 로직을 작성한 후에, 슈퍼 클래스의 post 메서드 호출
        return super().post(request, *args, **kwargs)
# Create your views here.
# class RegistrationAPIView(APIView):
#     permission_classes = (AllowAny,)
#     serializer_class = RegistrationSerializer
#     renderer_classes = (UserJSONRenderer,)
    
#     def post(self, request):
#         user = request.data
        
#         serializer = self.serializer_class(data=user)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# class CustomRegisterView(RegisterView):
#     serializer_class = CustomRegisterSerializer


# class LoginAPIView(APIView):
#     permission_classes = (AllowAny,)
#     renderer_classes = (UserJSONRenderer,)
#     serializer_class = LoginSerializer
    
#     # 1.
#     def post(self, request):
#         # 2.
#         user = request.data
        
#         # 3.
#         serializer = self.serializer_class(data=user)
#         serializer.is_valid(raise_exception=True)
        
#         # 4.
#         return Response(serializer.data, status=status.HTTP_200_OK)
    

# class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
#     permission_classes = (IsAuthenticated,)
#     renderer_classes = (UserJSONRenderer,)
#     serializer_class = UserSerializer
    
#     # 1.
#     def get(self, request, *args, **kwargs):
#         # 2.
#         serializer = self.serializer_class(request.user)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     # 3.
#     def patch(self, request, *args, **kwargs):
#         serializer_data = request.data
#         # 4.
#         serializer = self.serializer_class(
#             request.user, data=serializer_data, partial=True
#         )
        
#         serializer.is_valid(raise_exception=True)
#         # 5.
#         serializer.save()
        
#         return Response(serializer.data, status=status.HTTP_200_OK)