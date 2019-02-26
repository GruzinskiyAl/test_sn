from rest_framework import generics, mixins

from .models import (PostModel,
                     LikeModel,
                     User)
from .serializers import (PostSerializer,
                          LikeSerializer,
                          UserSerializer)





class PostList(generics.ListCreateAPIView):
    queryset = PostModel.objects.all()
    serializer_class = PostSerializer


