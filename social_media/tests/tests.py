from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

BASE_URL = reverse("social_media:profile-list")


class UnAuthenticatedUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_unauthenticated_user(self):
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="test123",
        )
        self.client.force_authenticate(user=self.user)

    def test_authenticated_user(self):
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
