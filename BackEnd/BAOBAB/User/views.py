from .api.serializers import UserSerializer
from .models import User
from rest_framework import viewsets

class UserViewSets(viewsets.ModelViewSet):
    queryset = User.object.all()
    serializer_class = UserSerializer
    lookup_field = 'id'
