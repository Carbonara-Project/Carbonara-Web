from rest_framework import permissions

class IsSelfUser(permissions.BasePermission):
    """
    Permission to check if the user data that need to be changed
    are owned by the user who owns the request token
    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user