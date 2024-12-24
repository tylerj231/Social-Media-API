import os
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify

from SocialMediaAPI import settings


class Profile(models.Model):

    class GenderChoices(models.TextChoices):
        MALE = "Male",
        FEMALE = "Female"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    bio = models.CharField(
        max_length=300,
        blank=True,
        null=True
    )
    gender = GenderChoices.choices

    profile_picture = models.ImageField(
        null=True,
        blank=True,
        upload_to="user_profile_image_path"
    )
    following = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="users",
    )

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def user_profile_image_path(self, filename):
        _, extension = os.path.splitext(filename)
        return os.path.join(
            "uploads/images/",
            f"{slugify(self.user.username)}-{uuid.uuid4()}{extension}"
        )


class Post(models.Model):
    title = models.CharField(
        max_length=100,
        unique=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts"
    )
    hashtag = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.title

class User(AbstractUser):

    def __str__(self):
        return self.username