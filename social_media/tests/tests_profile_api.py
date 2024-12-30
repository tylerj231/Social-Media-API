from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from social_media.models import Profile

from social_media.serializers import ProfileListSerializer, ProfileRetrieveSerializer


class ProfileAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="user@user.com",
            password="password123",
        )
        self.client.force_authenticate(user=self.user)

    def test_profile_list(self):
        Profile.objects.create(
            first_name="Don",
            last_name="Fry",
            bio="Bunch of sissies",
            gender="Male",
            user=self.user,
        )
        url = reverse("social_media:profile-list")
        response = self.client.get(url)
        profiles = Profile.objects.all()
        serializer = ProfileListSerializer(profiles, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_profile_detail(self):
        profile = Profile.objects.create(user=self.user)
        url = reverse("social_media:profile-detail", args=[profile.id])
        response = self.client.get(url)

        serializer = ProfileRetrieveSerializer(profile)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_profile_allowed(self):
        payload = {
            "first_name": "John",
            "last_name": "Doe",
            "user": self.user.id,
            "bio": "A bio",
        }
        url = reverse("social_media:profile-list")
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_profile_allowed(self):
        profile = Profile.objects.create(
            first_name="John",
            last_name="Doe",
            gender="Male",
            user=self.user,
            bio="A bio",
        )
        url = reverse("social_media:profile-detail", args=[profile.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
