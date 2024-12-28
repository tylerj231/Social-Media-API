from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from social_media.models import Post
from social_media.serializers import PostListSerializer, PostDetailSerializer


class PostsApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="password123",
        )
        self.client.force_authenticate(user=self.user)

    def test_post_create_allowed(self):
        payload = {
            "title": "Days gone by",
            "created_at": datetime.now(),
            "content": "Hi there!",
            "author": self.user.id,
            "hashtag": "#whatever",
        }
        url = reverse("social_media:post-list")
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_delete_allowed(self):
        post = Post.objects.create(
            title="Days gone by",
            content="Hi there!",
            author=self.user,
            hashtag="#whatever",
            created_at=datetime.now(),
        )
        url = reverse("social_media:post-detail", args=[post.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_post_list(self):
        Post.objects.create(
            title="Days gone by",
            content="Hi there!",
            author=self.user,
            hashtag="#whatever",
            created_at=datetime.now(),
        )
        posts = Post.objects.all()
        serializer = PostListSerializer(posts, many=True)
        url = reverse("social_media:post-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_post_detail(self):
        post = Post.objects.create(
            title="Days gone by",
            content="Hi there!",
            author=self.user,
            hashtag="#whatever",
            created_at=datetime.now(),
        )
        url = reverse(
            "social_media:post-detail",
            args=[
                post.id,
            ],
        )
        response = self.client.get(url)
        serializer = PostDetailSerializer(post)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
