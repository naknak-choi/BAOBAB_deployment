from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status

from Category.models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta :
        model = Category
        fields = '__all__'
        
    def validate(self,data):
        if data['is_main']:
            if not data['mainCategory_name'] is None:
                raise serializers.ValidationError('메인카테고리는 하위카테고리로 설정할 수 없습니다.')
            return data
        else:
            if data['mainCategory_name'] is None:
                raise serializers.ValidationError('메인카테고리를 지정해주세요')

            elif not Category.objects.filter(pk=data['mainCategory_name']).exists():
                raise serializers.ValidationError('메인카테고리가 존재하지 않습니다.')
            return data