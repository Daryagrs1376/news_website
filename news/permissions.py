from rest_framework import permissions



class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to delete it.
    """
    def has_object_permission(self, request, view, obj):
        # بررسی می‌کند که آیا کاربر درخواست‌دهنده صاحب شیء است یا خیر
        return obj.reporter == request.user
