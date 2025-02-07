from rest_framework import permissions


class IsOwnerUser(permissions.BasePermission):
    """Если пользователь владелец профиля"""

    def has_object_permission(self, request, view, obj):

        if obj.id == request.user.id:
            return True
        return False


class IsModer(permissions.BasePermission):
    """Если пользователь модератор"""

    def has_permission(self, request, view):

        return request.user.groups.filter(name="moders").exists()


class IsOwner(permissions.BasePermission):
    """Если пользователь владелец"""

    def has_object_permission(self, request, view, obj):

        if obj.owner == request.user:
            return True
        return False
