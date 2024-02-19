from rest_framework import permissions
from rest_framework.views import Request, View


class IsOwnerOrSuperUser(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj):
        return request.user == obj.user or request.user.is_superuser
