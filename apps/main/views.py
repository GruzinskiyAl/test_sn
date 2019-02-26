from rest_framework import generics, mixins

from .models import (PostModel,
                     LikeModel,
                     User)
from .serializers import (PostSerializer,
                          LikeSerializer,
                          UserSerializer,
                          UserCreateSerializer)


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    




class PostList(generics.ListCreateAPIView):
    queryset = PostModel.objects.all()
    serializer_class = PostSerializer


