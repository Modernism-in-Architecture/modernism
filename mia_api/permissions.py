from rest_framework.permissions import BasePermission, IsAdminUser, IsAuthenticated


class IsAuthenticatedOrAdminUser(BasePermission):
    """
    Custom permission to allow access if the user is authenticated OR is an admin.
    """

    def has_permission(self, request, view):
        return IsAuthenticated().has_permission(
            request, view
        ) or IsAdminUser().has_permission(request, view)
