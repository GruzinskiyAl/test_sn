from django.contrib import admin
from django.urls import path

from apps.main import views

urlpatterns = [
    path("post/", views.PostList.as_view(), name="post-list"),

    path("account/create/", views.UserCreateView.as_view(), name="create-user")
]
