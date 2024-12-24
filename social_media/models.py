import os
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify


class User(AbstractUser):
    bio = models.CharField(
        max_length=300,
        blank=True,
        null=True
    )
    profile_picture = models.ImageField(
        null=True,
        blank=True,
        upload_to="user_profile_image_path"
    )

    def __str__(self):
        return self.username

    def user_profile_image_path(self, filename):
        _, extension = os.path.splitext(filename)
        return os.path.join(
            "uploads/images/",
            f"{slugify(self.username)}-{uuid.uuid4()}{extension}"
        )


class Post(models.Model):
    title = models.CharField(
        max_length=100,
        unique=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField(max_length=700)
    users = models.ManyToManyField(User, related_name="posts")

    def __str__(self):
        return self.title

class Follow(models.Model):
    users = models.ManyToManyField(User, related_name="followers")