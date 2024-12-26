from rest_framework.viewsets import ModelViewSet

from social_media.models import Profile, Post
from social_media.serializers import (
    ProfileSerializer,
    PostSerializer,
    PostListSerializer,
    PostDetailSerializer
)


class ProfileViewSet(ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer
        if self.action == "retrieve":
            return PostDetailSerializer
        return PostSerializer
