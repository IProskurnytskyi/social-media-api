from django.urls import path, include
from rest_framework import routers

from user.views import (
    CreateUserView,
    ManageUserView,
    ProfileView,
    CreateProfileViewSet,
    HashtagView,
    PostViewSet
)

router = routers.DefaultRouter()
router.register(
    "create_profile", CreateProfileViewSet, basename="create_profile"
)
router.register("profiles", ProfileView, basename="profiles")
router.register("posts", PostViewSet)


urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("me/", ManageUserView.as_view(), name="manage"),
    path("hashtags", HashtagView.as_view(), name="hashtags"),
    path("", include(router.urls)),
]

app_name = "user"
