from rest_framework.permissions import BasePermission


class IsCustomer(BasePermission):
    message = "You are not customer"

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.role == 'customer')


class IsAdmin(BasePermission):
    message = "You are not admin"

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.role == 'admin')
