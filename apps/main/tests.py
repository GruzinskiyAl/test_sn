import json
from django.urls import reverse as _
from rest_framework.test import (APITestCase,
                                 APIClient,
                                 APIRequestFactory,
                                 force_authenticate)

from .models import (User,
                     PostModel,
                     LikeModel)
from .views import (PostList)


class TestPostAPI(APITestCase):
    fixtures = [
        "users.json",
        "posts.json"
    ]

    def setUp(self):
        self.factory = APIRequestFactory()
        self.admin_user = User.objects.get(email="admin@email.com")
        self.simple_user = User.objects.get(email="user1@email.com")

    def test_init_data(self):
        self.assertEqual(User.objects.all().count(), 2)
        self.assertEqual(PostModel.objects.all().count(), 3)

    def test_post_list(self):
        req = self.factory.get(_("post-list"))
        view = PostList.as_view()
        res = view(req)
        self.assertEqual(res.status_code, 200)

    def test_post_creating(self):
        data = {
            "title": "New post",
            "text": "Some Text"
        }
        view = PostList.as_view()
        req = self.factory.post(_("post-list"), data=json.dumps(data), content_type="application/json")
        res = view(req)
        self.assertEqual(res.status_code, 401)

        force_authenticate(req, user=self.simple_user)
        res = view(req)
        self.assertEqual(res.status_code, 201)

    def test_like_post(self):
        pass
