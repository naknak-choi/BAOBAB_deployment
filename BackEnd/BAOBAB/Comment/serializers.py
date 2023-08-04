from .models import Comment
from rest_framework import serializers

# serializers.py
# to_represenstation을 오버라이딩해서 화면에 출력하는 방법
class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, instance):
        serializer = self.parent.parent.__class__(instance, context=self.context)
        return serializer.data


class CommentSerializer(serializers.ModelSerializer):
    reply = serializers.SerializerMethodField()
    # reply = RecursiveSerializer(many=True, read_only=True)
    product = serializers.SlugRelatedField(queryset=Comment.objects.all(), slug_field='name')
    
    class Meta:
        model = Comment
        fields = ('id', 'user', 'product', 'parent', 'body', 'reply')
    
    def get_reply(self, instance):
    	# recursive
        serializer = self.__class__(instance.reply, many=True)
        serializer.bind('', self)
        return serializer.data