from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        # Allow read permissions to anyone
        if request.method in permissions.SAFE_METHODS:
            return True

        # Restrict write permissions to authenticated users
        return request.user and request.user.is_authenticated and request.user.is_staff
