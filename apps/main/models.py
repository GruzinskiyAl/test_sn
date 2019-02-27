from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserAccountManager(BaseUserManager):

    def _create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError("Email must be provided")
        if not password:
            raise ValueError("Password must be provided")

        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email=None, password=None, **kwargs):
        return self._create_user(email, password, **kwargs)

    def create_superuser(self, email, password, **kwargs):
        kwargs["is_staff"] = True
        kwargs["is_superuser"] = True

        return self._create_user(email, password, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    objects = UserAccountManager()

    email = models.EmailField("email", unique=True, null=False, blank=False)
    is_staff = models.BooleanField('staff status', default=False)
    is_active = models.BooleanField('active', default=True)

    def __str__(self):
        return self.email


class PostModel(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, null=False, blank=False)
    title = models.CharField(max_length=256, null=False, blank=False)
    text = models.TextField(null=False, blank=False)

    def __str__(self):
        return f'{self.id}__{self.title[:64]}...'


class LikeModel(models.Model):
    user = models.ForeignKey("User", on_delete=models.SET_NULL, null=True, blank=True)
    post = models.ForeignKey("PostModel", on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f'{self.user}__{self.post.id}'
