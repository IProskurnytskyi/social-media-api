from django.contrib.auth import get_user_model
from rest_framework import serializers

from user.models import User, Hashtag, Post, Follow


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "password",
            "is_staff",
        )
        read_only_fields = ("is_staff",)
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data: dict) -> User:
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ("id", "users")


class UpdateUserSerializer(serializers.ModelSerializer):
    followings = FollowSerializer(many=True, read_only=False, required=False)

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "password",
            "is_staff",
            "first_name",
            "last_name",
            "age",
            "created_at",
            "bio",
            "gender",
            "company",
            "location",
            "picture",
            "followings"
        )
        read_only_fields = ("is_staff",)
        extra_kwargs = {
            "password": {
                "write_only": True,
                "min_length": 5,
                "required": False
            }
        }

    def update(self, instance: User, validated_data: dict) -> User:
        """Update a user, set the password correctly and return it"""
        password = validated_data.pop("password", None)
        users_ids = validated_data.pop("followings", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)

        if users_ids:
            follow_objects = []
            for user_id in users_ids[0].get("users"):
                follow_obj, _ = Follow.objects.get_or_create(id=user_id.id)
                follow_objects.append(follow_obj.id)
            user.followings.set(follow_objects)

        user.save()
        return user


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "created_at",
            "picture",
            "full_name"
        )


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ("id", "name")


class PostSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)

    class Meta:
        model = Post
        fields = ("id", "text", "hashtags", "image", "user")


class PostRetrieveSerializer(PostSerializer):
    hashtags = HashtagSerializer(read_only=True, many=True)
