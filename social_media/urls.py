from django.urls import include, path

from rest_framework import routers

from social_media.views import ProfileViewSet, PostViewSet

router = routers.DefaultRouter()
router.register("profiles", ProfileViewSet)
router.register("posts", PostViewSet)

app_name = "social_media"

urlpatterns = [
    path("", include(router.urls)),
]
