from django.db import models

from django.contrib.auth.models import User
# Create your models here.


class PostModel(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    title = models.CharField(max_length=256, null=False, blank=False)
    text = models.TextField(null=False, blank=False)

class LikeModel(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    post = models.ForeignKey("PostModel", on_delete=models.CASCADE)