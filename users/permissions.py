from rest_framework.permissions import BasePermission


class IsModer(BasePermission):

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moderator").exists()

    def has_object_permission(self, request, view, obj):
        return request.user.groups.filter(name="moderator").exists()


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsSelfUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user
