from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """ Если пользователь владелец профиля """

    def has_object_permission(self, request, view, obj):

        if obj.id == request.user.id:
            return True
        return False
