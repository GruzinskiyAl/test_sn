from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from apps.main import views

urlpatterns = [
    path("post/", views.PostListView.as_view(), name="post-list"),
    path("post/like/", views.SetLikeView.as_view(), name="like-post"),
    # path("post/unlike/", views.UnsetLikeView.as_view(), name="unlike-post"),

    path("account/create/", views.UserCreateView.as_view(), name="create-user"),
    path("account/token/", TokenObtainPairView.as_view(), name="token-get-pair"),
    path("account/token/refresh/", TokenRefreshView.as_view(), name="token-refresh")
]
