from rest_framework import permissions



class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to delete it.
    """
    def has_object_permission(self, request, view, obj):
        # بررسی می‌کند که آیا کاربر درخواست‌دهنده صاحب شیء است یا خیر
        return obj.reporter == request.user
class IsAdminUserOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only admin users to access the view.
    """

    def has_permission(self, request, view):
        # اگر درخواست GET باشد و کاربر ادمین باشد، اجازه می‌دهد
        return request.user and request.user.is_staff