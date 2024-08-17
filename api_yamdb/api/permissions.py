from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsAdmin(permissions.BasePermission):
    """Проверка на то, является ли пользователь администратором."""

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_admin())


class ReadonlyOrAdmin(permissions.BasePermission):
    """Проверка на права доступа пользователя."""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                and request.user.is_admin())


class ReadonlyOrOwnerOrStaff(permissions.BasePermission):
    """Проверка на то, является ли пользователь владельцем."""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                and (obj.author == request.user
                     or request.user.is_admin_or_moderator()))
