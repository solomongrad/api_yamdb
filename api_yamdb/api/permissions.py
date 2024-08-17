from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class OwnerOrAdmin(permissions.BasePermission):
    """Проверка является ли пользователь владельцем или администратором."""

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_admin())

    def has_object_permission(self, request, view, obj):
        return (obj == request.user
                or request.user.is_admin() or request.user.is_moderator())


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
                     or request.user.is_admin()
                     or request.user.is_moderator()))
