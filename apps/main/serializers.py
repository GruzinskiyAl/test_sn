import requests
from django.conf import settings
from django.db import IntegrityError
from rest_framework import serializers

from .models import (PostModel,
                     LikeModel,
                     User)

import clearbit


class UserCreateSerializer(serializers.ModelSerializer):
    hunter_verified = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            "email",
            "full_name",
            "given_name",
            "family_name",
            "location",
            "bio",
            "site",
            "password",
            "hunter_verified"
        )

        read_only_fields = ("full_name",
                            "given_name",
                            "family_name",
                            "location",
                            "bio",
                            "site")

        extra_kwargs = {
            "password": {
                "write_only": True
            }
        }

    def get_hunter_verified(self, obj):
        try:
            email = obj["email"]
        except (AttributeError, TypeError):
            email = obj.email
        except KeyError:
            return False
        return self._check_email(email)

    def _check_email(self, email):
        """
        Check email by hunter api if
        :param email:
        :return: boolean value
        """
        data = {
            "email": email,
            "api_key": settings.HUNTER_API_KEY
        }
        res = requests.get(settings.HUNTER_API, params=data)
        if res.json()["data"]["score"] > 50:
            return True
        return False

    def _get_user_data(self, email):
        """
        Get users data from clearbit by email
        :param email:
        :return: dict of users data
        """
        clearbit.key = settings.CLEARBIT_API_KEY
        person = clearbit.Person.find(email=email, stream=True)
        if person:
            data = {
                "full_name": person["name"]["fullName"],
                "given_name": person["name"]["givenName"],
                "family_name": person["name"]["familyName"],
                "location": person["location"],
                "bio": person["bio"],
                "site": person["site"],
            }
            return data
        return {}

    def create(self, validated_data):
        """
        User creating method
        p.s. not sure about updating validated data in this method
        """
        email = validated_data["email"]
        password = validated_data["password"]
        user_obj = User(
            email=email
        )
        user_obj.set_password(password)
        user_obj.save()

        user_data = self._get_user_data(email)
        User.objects.filter(pk=user_obj.pk).update(**user_data)
        validated_data.update(user_data)

        return validated_data


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
        read_only_fields = ("user", )

    def save(self, **kwargs):
        """
        Setting author of post on the fly
        """
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
        """
        user and post are unique together, so exception handled
        """
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



