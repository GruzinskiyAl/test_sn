from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly

from .models import (PostModel,
                     LikeModel,
                     User)
from .serializers import (PostCreateSerializer,
                          PostReadSerializer,
                          LikeSerializer,
                          UserSerializer,
                          UserCreateSerializer)


class UserCreateView(generics.CreateAPIView):
    permission_classes = (AllowAny, )

    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    

class PostListView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )

    queryset = PostModel.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return PostReadSerializer
        return PostCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, 400)


class SetLikeView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = LikeSerializer

    def post(self, request,  *args, **kwards):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.set_like()
            return Response(status=201)
        return Response(serializer.errors, status=400)


class RemoveLikeView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = LikeSerializer

    def post(self, request,  *args, **kwards):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.remove_like()
            return Response(status=204)
        return Response(serializer.errors, status=400)

