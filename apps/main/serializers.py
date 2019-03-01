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
        fields = "__all__"


class PostReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostModel
        fields = "__all__"


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeModel
        fields = "__all__"
