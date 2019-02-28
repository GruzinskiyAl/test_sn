from django.urls import path

from apps.main import views

urlpatterns = [
    path("post/", views.PostListView.as_view(), name="post-list"),
    path("post/like/", views.SetLikeView(), name="like-post"),
    path("post/unlike/", views.UnsetLikeView.as_view(), name="unlike-post"),

    path("account/create/", views.UserCreateView.as_view(), name="create-user"),
    path("account/login", views.LoginView.as_view(), name="login-user")
]
