from .api.serializers import *
from User.api.serializers import *

from rest_framework import generics
from rest_framework import viewsets

from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny

from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import *

class BookStaffViewSet(viewsets.ModelViewSet):
    queryset = BookInfo.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = BookStaffSerializer
    parser_classes = [MultiPartParser, FileUploadParser]
    
class BookUserViewSet(viewsets.ModelViewSet):
    queryset = BookInfo.objects.all()
    serializer_class = BookUserSerializer
    permission_classes = [IsAuthenticated]