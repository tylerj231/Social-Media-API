from rest_framework import serializers
from social_media.models import Profile, Post


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "user",
            "first_name",
            "last_name",
            "bio",
            "gender",
            "profile_picture",
            "following",
        )


class ProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "user",
            "first_name",
            "last_name",
            "profile_picture",
            "follow",
            "followers",
        )


class ProfileRetrieveSerializer(serializers.ModelSerializer):
    following = serializers.SlugRelatedField(
        slug_field="email", read_only=True, many=True
    )
    followers = serializers.SerializerMethodField()

    user = serializers.CharField(read_only=True, source="user.email")

    class Meta:
        model = Profile
        fields = (
            "user",
            "full_name",
            "gender",
            "profile_picture",
            "following",
            "followers",
        )

    @staticmethod
    def get_followers(obj):
        return [follower.user.email for follower in obj.user.following.all()]


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
        source="author.email",
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
