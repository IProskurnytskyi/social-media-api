from typing import Type

from django.db.models import QuerySet
from rest_framework import generics, viewsets, mixins
from rest_framework.viewsets import GenericViewSet

from user.models import User, Profile
from user.serializers import (
    UserSerializer,
    ProfileSerializer,
    ProfileListSerializer
)


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self) -> User:
        return self.request.user


class ProfileView(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def get_serializer_class(self) -> Type:
        if self.action == "list":
            return ProfileListSerializer

        return ProfileSerializer


class CreateProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def get_queryset(self) -> QuerySet:
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer) -> None:
        serializer.save(user=self.request.user)
