import json
from django.urls import reverse as _
from rest_framework.test import (APITransactionTestCase,
                                 APIClient,
                                 APIRequestFactory,
                                 force_authenticate)

from .models import (User,
                     PostModel,
                     LikeModel)
from .views import (PostListView,
                    SetLikeView,
                    RemoveLikeView,
                    UserCreateView)


class TestAPI(APITransactionTestCase):
    fixtures = [
        "users.json",
        "posts.json",
        "likes.json"
    ]

    def setUp(self):
        self.factory = APIRequestFactory()
        self.admin_user = User.objects.get(email="admin@email.com")
        self.simple_user = User.objects.get(email="user1@email.com")

        self.init_users_count = User.objects.all().count()
        self.init_posts_count = PostModel.objects.all().count()
        self.init_likes_count = LikeModel.objects.all().count()

    def test_post_list(self):
        req = self.factory.get(_("post-list"))
        view = PostListView.as_view()
        res = view(req)
        self.assertEqual(res.status_code, 200)

    def test_post_creating(self):
        data = {
            "title": "New post",
            "text": "Some Text"
        }
        view = PostListView.as_view()
        req = self.factory.post(_("post-list"), data=json.dumps(data), content_type="application/json")
        res = view(req)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(PostModel.objects.all().count(), self.init_posts_count)

        force_authenticate(req, user=self.simple_user)
        res = view(req)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(PostModel.objects.all().count(), self.init_posts_count + 1)
        self.assertTrue(res.data["id"])
        self.assertTrue(res.data["user"])

    def test_like_post_unauthenticated(self):
        data = {
            "post": 1
        }
        view = SetLikeView.as_view()
        req = self.factory.post(_("like-post"), data=json.dumps(data), content_type="application/json")
        res = view(req)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(LikeModel.objects.all().count(), self.init_likes_count)

    def test_like_post_authenticated(self):
        data = {
            "post": 1
        }
        view = SetLikeView.as_view()
        req = self.factory.post(_("like-post"), data=json.dumps(data), content_type="application/json")
        force_authenticate(req, user=self.simple_user)
        res = view(req)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(LikeModel.objects.all().count(), self.init_likes_count + 1)

    def test_like_liked_post(self):
        data = {
            "post": 2
        }
        view = SetLikeView.as_view()
        req = self.factory.post(_("like-post"), data=json.dumps(data), content_type="application/json")
        force_authenticate(req, user=self.simple_user)
        res = view(req)
        likes_count = LikeModel.objects.all().count()
        self.assertEqual(res.status_code, 201)
        self.assertEqual(likes_count, self.init_likes_count)

    def test_unlike_post_unauthenticated(self):
        data = {
            "post": 2
        }
        view = RemoveLikeView.as_view()
        req = self.factory.post(_("unlike-post"), data=json.dumps(data), content_type="application/json")
        res = view(req)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(LikeModel.objects.all().count(), self.init_likes_count)

    def test_unlike_post_authenticated(self):
        data = {
            "post": 2
        }
        view = RemoveLikeView.as_view()
        req = self.factory.post(_("unlike-post"), data=json.dumps(data), content_type="application/json")
        force_authenticate(req, user=self.simple_user)
        res = view(req)
        self.assertEqual(res.status_code, 204)
        self.assertEqual(LikeModel.objects.all().count(), self.init_likes_count - 1)

    def test_unlike_not_liked_post(self):
        data = {
            "post": 1
        }
        view = RemoveLikeView.as_view()
        req = self.factory.post(_("unlike-post"), data=json.dumps(data), content_type="application/json")
        force_authenticate(req, user=self.simple_user)
        res = view(req)
        self.assertEqual(res.status_code, 204)
        self.assertEqual(LikeModel.objects.all().count(), self.init_likes_count)

    def test_user_registration(self):
        data = {
            "email": "test@email.com",
            "password": "test"
        }
        view = UserCreateView.as_view()
        req = self.factory.post(_("create-user"), data=json.dumps(data), content_type="application/json")
        res = view(req)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(User.objects.all().count(), self.init_users_count + 1)

    def test_user_registration_email_already_exist(self):
        data = {
            "email": "user1@email.com",
            "password": "test"
        }
        view = UserCreateView.as_view()
        req = self.factory.post(_("create-user"), data=json.dumps(data), content_type="application/json")
        res = view(req)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(User.objects.all().count(), self.init_users_count)


class TestAuthAPI(APITransactionTestCase):
    fixtures = (
        'users.json',
        "posts.json"
    )

    def setUp(self):
        self.client = APIClient()

        self.email = "test@email.com"
        self.password = "qwerty12345"
        self.data = {
            "email": self.email,
            "password": self.password
        }

    def test_user_authentication(self):
        user = User.objects.create_user(email=self.email, password=self.password)
        user.is_active = True
        user.save()

        res = self.client.post(_("token-get-pair"), data=json.dumps(self.data), content_type="application/json")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 2)

        token = res.data["access"]
        data = {
            "title": "new title",
            "text": "new text"
        }
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        res = self.client.post(_("post-list"), data=json.dumps(data), content_type="application/json")
        self.assertEqual(res.status_code, 201)

    def test_user_authentication_incorrect_data(self):
        user = User.objects.create_user(email=self.email, password=self.password)
        user.is_active = True
        user.save()

        data = {
            "email": self.email,
            "password": "incorrect"
        }
        res = self.client.post(_("token-get-pair"), data=json.dumps(data), content_type="application/json")
        self.assertEqual(res.status_code, 400)
