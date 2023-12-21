from typing import Type

from django.contrib.auth import logout
from django.db.models import QuerySet
from rest_framework import generics, viewsets, status, mixins, permissions
from rest_framework.decorators import api_view, action
from rest_framework.request import Request
from rest_framework.response import Response

from user import permission
from user.models import User, Hashtag, Post, Follow
from user.serializers import (
    CreateUserSerializer,
    UpdateUserSerializer,
    UserListSerializer,
    HashtagSerializer,
    PostSerializer,
    PostRetrieveSerializer
)


class UserViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = UserListSerializer
    queryset = User.objects.prefetch_related("followings")

    def get_object(self) -> User:
        return self.request.user

    def get_serializer_class(self) -> Type:
        if self.action == "create":
            return CreateUserSerializer
        elif self.action in ("retrieve", "update"):
            return UpdateUserSerializer
        return UserListSerializer

    @action(detail=True, methods=["GET"], url_path="followings")
    def get_following_users(self, request, pk=None) -> Response:
        user = self.get_object()
        following_objects = user.followings.all()
        following_ids = [following_object.id for following_object in following_objects]
        following_users = User.objects.filter(id__in=following_ids)

        serializer = UserListSerializer(following_users, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["GET"], url_path="followers")
    def get_followers(self, request, pk=None) -> Response:
        user = self.get_object()
        follow_user_object = Follow.objects.get(id=user.id)
        followers = User.objects.filter(followings=follow_user_object)

        serializer = UserListSerializer(followers, many=True)
        return Response(serializer.data)

    def get_queryset(self) -> QuerySet:
        user_id = self.request.query_params.get("id")
        first_name = self.request.query_params.get("first_name")
        last_name = self.request.query_params.get("last_name")

        queryset = self.queryset

        if user_id:
            queryset = queryset.filter(id=user_id)

        if first_name:
            queryset = queryset.filter(first_name__icontains=first_name)

        if last_name:
            queryset = queryset.filter(last_name__icontains=last_name)

        return queryset


class HashtagView(generics.ListCreateAPIView):
    serializer_class = HashtagSerializer
    queryset = Hashtag.objects.all()


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.prefetch_related("hashtags").select_related("user")
    permission_classes = [permissions.IsAuthenticated, permission.IsOwnerOrReadOnly]

    def perform_create(self, serializer) -> None:
        serializer.save(user=self.request.user)

    def get_object(self) -> Post:
        user = self.request.user
        following_objects = user.followings.all()
        following_ids = [following_object.id for following_object in following_objects]
        following_ids.append(user.id)
        posts = Post.objects.filter(user_id__in=following_ids)
        specific_post = posts.filter(pk=self.kwargs["pk"]).first()

        return specific_post

    def get_serializer_class(self) -> Type:
        if self.action == "retrieve":
            return PostRetrieveSerializer

        return PostSerializer

    def get_queryset(self) -> QuerySet:
        hashtag_ids = self.request.query_params.get("ids")
        queryset = self.queryset

        if hashtag_ids:
            ids = [int(hashtag_id) for hashtag_id in hashtag_ids.split(",")]
            queryset = queryset.filter(hashtags__id__in=ids)

        return queryset.distinct()


@api_view(["GET"])
def user_logout(request: Request) -> Response:
    logout(request)
    return Response(
        {"message": "You have been logged out."}, status=status.HTTP_200_OK
    )
