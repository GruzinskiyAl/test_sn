from django.contrib import admin
from django.urls import path

from apps.main import views

urlpatterns = [
    path("", views.PostList.as_view(), name="post-list"),
]
