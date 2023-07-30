from rest_framework.permissions import IsAdminUser
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from .api.serializers import *
# Create your views here.

class CreateCategoryView(generics.CreateAPIView):
    serializer_class = CreateCategorySerializer
    permission_classes = [IsAdminUser]
    
    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            is_main = data.get('is_main')
            mainCategory_name = data.get('mainCategory_name')
            
            # print(mainCategory_name == "")
            # print("is_main : " + is_main)
            if is_main:
                if not mainCategory_name == "":
                    return Response({'error': '메인카테고리는 하위카테고리로 설정할 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                if mainCategory_name == "":
                    return Response({'error': '메인카테고리를 지정해주세요'}, status=status.HTTP_400_BAD_REQUEST)
                
                elif not Category.objects.filter(pk=mainCategory_name).exists():
                    return Response({'error': '메인카테고리가 존재하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
                
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)