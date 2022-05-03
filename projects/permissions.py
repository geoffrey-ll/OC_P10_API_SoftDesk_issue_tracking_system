from rest_framework.exceptions import NotAuthenticated
from rest_framework.permissions import BasePermission, SAFE_METHODS


class AuthorPermission(BasePermission):
    # message = "blabla"
    NotAuthenticated(detail="TEST")

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        try:
            if obj.author_user == request.user:
                return True
        except:
            pass
        try:
            if obj.user == request.user:
                return True
        except:
            pass
        return False
        # return obj.author_user == request.user
