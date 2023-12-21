from rest_framework import permissions

SAFE_METHODS = ("GET", "POST", "HEAD", "OPTIONS")


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj) -> bool:
        if request.method in SAFE_METHODS:
            return True

        return obj.user == request.user
