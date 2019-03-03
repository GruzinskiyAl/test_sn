from django.db import IntegrityError
from rest_framework import serializers

from .models import (PostModel,
                     LikeModel,
                     User)


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            "password"
        )
        extra_kwargs = {
            "password": {
                "write_only": True
            },
        }

    def create(self, validated_data):
        email = validated_data["email"]
        password = validated_data["password"]
        user_obj = User(
            email=email
        )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostModel
        fields = (
            "id",
            "user",
            "title",
            "text",
            "published_date"
        )
        extra_kwargs = {
            "user": {
                "read_only": True
            },
        }

    def save(self, **kwargs):
        self.validated_data["user"] = self.context["request"].user
        super(PostCreateSerializer, self).save(**kwargs)


class PostReadSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    liked_by_user = serializers.SerializerMethodField()

    class Meta:
        model = PostModel
        fields = (
            "id",
            "user",
            "title",
            "text",
            "published_date",
            "likes_count",
            "liked_by_user"
        )

    def get_likes_count(self, obj):
        return LikeModel.objects.filter(post=obj).count()

    def get_liked_by_user(self, obj):
        user = self.context["request"].user
        try:
            return True if LikeModel.objects.filter(user=user, post=obj).count() > 0 else False
        except TypeError:
            return False


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeModel
        fields = (
            "post",
        )

    def _get_request_user(self):
        return self.context["request"].user

    def set_like(self):
        try:
            LikeModel.objects.create(
                user=self._get_request_user(),
                post=self.validated_data["post"]
            )
        except(IntegrityError, ):
            return False

    def remove_like(self):
        try:
            LikeModel.objects.get(
                user=self._get_request_user(),
                post=self.validated_data["post"]
            ).delete()
        except (LikeModel.DoesNotExist, ):
            return False



