from rest_framework import permissions
from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.permissions import BasePermission



class IsNotAuthenticated(BasePermission):
    """
    اجازه نمی‌دهد کاربرانی که لاگین کرده‌اند، به این ویو دسترسی داشته باشند.
    """
    def has_permission(self, request, view):
        return not request.user.is_authenticated

class NewsSearchView(APIView):

    @permission_classes([AllowAny])  # در اینجا از دکوراتور برای تعریف پرمیشن استفاده می‌کنیم
    def get(self, request):
        # عملیات جستجو
        return Response({"message": "News search works!"})


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