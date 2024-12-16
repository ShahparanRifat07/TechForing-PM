import rest_framework.permissions as permissions


class IsProjectOwnerOrAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.is_owner_or_admin(request.user)
