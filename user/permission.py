from rest_framework import permissions

SAFE_METHODS_WITH_POST = ("GET", "POST", "HEAD", "OPTIONS")


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj) -> bool:
        if request.method in SAFE_METHODS_WITH_POST:
            return True

        return obj.user == request.user
