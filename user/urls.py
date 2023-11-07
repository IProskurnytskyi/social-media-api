from django.urls import path, include
from rest_framework import routers

from user.views import (
    CreateUserView,
    ManageUserView,
    ProfileView,
    CreateProfileViewSet
)

router = routers.DefaultRouter()
router.register(
    "create_profile", CreateProfileViewSet, basename="create_profile"
)
router.register("profiles", ProfileView, basename="profiles")


urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("me/", ManageUserView.as_view(), name="manage"),
    path("", include(router.urls)),
]

app_name = "user"
