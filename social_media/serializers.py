from rest_framework import serializers

from social_media.models import Profile, Post


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "user",
            "bio",
            "gender",
            "profile_picture",
            "following",
        )

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "author",
            "hashtag",
            "content",
        )

class PostListSerializer(PostSerializer):
    author = serializers.CharField(
        read_only=True,
        source="author.username",
    )
    class Meta:
        model = Post
        fields = PostSerializer.Meta.fields

class PostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            "title",
            "created_at",
            "author",
            "content",
            "hashtag",
        )