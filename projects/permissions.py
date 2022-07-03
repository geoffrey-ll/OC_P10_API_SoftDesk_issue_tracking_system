from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from rest_framework.permissions import BasePermission, SAFE_METHODS

from .messages_error import (
    MESSAGE_PERMISSION_DENIED,
    MESSAGE_PERMISSION_NOT_AUTHENTICATED
)
from .models import Contributor


class AssignPermission(BasePermission):
    """
    Permission par défaut.
    Vérifie l'authentification et redirige vers les permissions associées au
    role de l'utilisateur
    """

    @staticmethod
    def get_my_role(request, view):
        """Renvoi le rôle qu'a l'utilisateur dans le project"""
        if view.__class__.__name__ == "ProjectViewSet":
            project_id = view.kwargs["pk"]
        else:
            project_id = view.kwargs["project_pk"]

        return Contributor.objects.get(
            project=project_id, user=request.user
        ).role

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if view.__class__.__name__ == "ProjectViewSet" \
                    and view.detail == False:
                return True

            else:
                try:
                    my_role = self.get_my_role(request, view)
                except:
                    raise PermissionDenied(detail=MESSAGE_PERMISSION_DENIED)

                if my_role == 'm':
                    return ManagerPermission().has_permission(
                        request, view
                    )
                if my_role == 'c':
                    return ContributorPermission().has_permission(
                        request, view
                    )
        raise NotAuthenticated(detail=MESSAGE_PERMISSION_NOT_AUTHENTICATED)

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            try:
                my_role = self.get_my_role(request, view)
            except:
                raise PermissionDenied(detail=MESSAGE_PERMISSION_DENIED)

            if my_role == 'm':
                return ManagerPermission().has_object_permission(
                    request, view, obj
                )
            if my_role == 'c':
                return ContributorPermission().has_object_permission(
                    request, view, obj
                )
        raise NotAuthenticated(detail=MESSAGE_PERMISSION_NOT_AUTHENTICATED)


class ManagerPermission(BasePermission):
    """Permissions pour les managers de project"""

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if view.__class__.__name__ == "ContributorViewSet" \
                or view.__class__.__name__ == "ProjectViewSet":
            return True
        if request.user != obj.authorg_user:
            return request.method in SAFE_METHODS
        return True


class ContributorPermission(BasePermission):
    """Permissions pour les contributeurs (non manager) de project"""

    def has_permission(self, request, view):
        if view.__class__.__name__ is "ContributorViewSet":
            return request.method in SAFE_METHODS
        return True

    def has_object_permission(self, request, view, obj):
        if view.__class__.__name__ == "ContributorViewSet":
            return request.method in SAFE_METHODS

        if request.user != obj.author_user:
            return request.method in SAFE_METHODS
        return True
