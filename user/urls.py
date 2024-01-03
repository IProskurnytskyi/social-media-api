from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from user.views import (
    UserViewSet,
    HashtagView,
    PostViewSet,
    user_logout,
)


user_list = UserViewSet.as_view({
    "get": "list"
})

user_detail = UserViewSet.as_view({
    "get": "retrieve",
    "put": "update",
    "delete": "destroy"
})

following_users = UserViewSet.as_view({
    "get": "get_following_users"
})

followers = UserViewSet.as_view({
    "get": "get_followers"
})

router = routers.DefaultRouter()
router.register("posts", PostViewSet)

urlpatterns = [
    path("register/", UserViewSet.as_view({"post": "create"}), name="create"),
    path("me/", user_detail, name="manage"),
    path("profiles/", user_list, name="profiles"),
    path("me/followings/", following_users, name="followings"),
    path("me/followers/", followers, name="followers"),
    path("logout/", user_logout, name="logout"),
    path("hashtags/", HashtagView.as_view(), name="hashtags"),
    path("", include(router.urls)),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]

app_name = "user"
