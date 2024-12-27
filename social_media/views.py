from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.viewsets import ModelViewSet

from social_media.models import Profile, Post
from social_media.permissions import (
    IsOwnerOrReadOnly,
    IsAuthorOrReadOnly
)
from social_media.serializers import (
    ProfileSerializer,
    PostSerializer,
    PostListSerializer,
    PostDetailSerializer,
    ProfileRetrieveSerializer,
    ProfileListSerializer,
)


class ProfileViewSet(ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = self.queryset.prefetch_related("user", "following")
        gender = self.request.query_params.get("gender", None)
        first_name = self.request.query_params.get("first_name", None)
        last_name = self.request.query_params.get("last_name", None)

        if first_name:
            queryset = queryset.filter(first_name__icontains=first_name)
        if last_name:
            queryset = queryset.filter(last_name__icontains=last_name)
        if gender is not None:
            queryset = queryset.filter(gender__icontains=gender)

        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return ProfileListSerializer
        if self.action == "retrieve":
            return ProfileRetrieveSerializer
        return ProfileSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="first_name",
                type=str,
                description="Filter profiles by first_name. EX: /profiles?first_name=Taras",
            ),
            OpenApiParameter(
                name="last_name",
                type=str,
                description="Filter profiles by last_name. EX: /profiles?last_name=Potato",
            ),
            OpenApiParameter(
                name="gender",
                type=str,
                description="Filter profiles by gender. EX: /profiles?gender=Male",
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        queryset = self.queryset.select_related("author")
        hashtag = self.request.query_params.get("hashtag")
        title = self.request.query_params.get("title")

        if hashtag:
            queryset = queryset.filter(hashtag__icontains=hashtag)
        if title:
            queryset = queryset.filter(title__icontains=title)

        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer
        if self.action == "retrieve":
            return PostDetailSerializer
        return PostSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="hashtag",
                type=str,
                description="Filter posts by hashtag. EX: /posts?hashtag=youdon'tknowme",
            ),
            OpenApiParameter(
                name="title",
                type=str,
                description="Filter posts by title. EX: /posts?title=How I met your mother",
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
