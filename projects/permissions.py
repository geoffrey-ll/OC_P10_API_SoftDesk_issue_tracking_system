from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from rest_framework.permissions import BasePermission, SAFE_METHODS


from .messages_error import (
    MESSAGE_PERMISSION_DENIED,
    MESSAGE_PERMISSION_NOT_AUTHENTICATED
)
from .models import Contributor, Project


class AssignPermission(BasePermission):
    def get_my_role(self, request, view):
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
            # Lignes à remettre dans le has_object ??
            # Le print ne s'affiche que lorsqu'on est dans un 'detail', pas dans une 'list'
            # Le has_object_permission n'est finalement appelé que lors des 'detail' ou pas ?????
            #
            # if view.__class__.__name__ == "ProjectViewSet" \
            #         and view.detail == True:
            #     print(f"\nPASSÉ PAR ICI\n")
            #     return True
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
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if view.__class__.__name__ == "ContributorViewSet" \
                or view.__class__.__name__ == "ProjectViewSet":
            return True

        if request.user != obj.author_user:
            return request.method in SAFE_METHODS


class ContributorPermission(BasePermission):
    def has_permission(self, request, view):
        if view.__class__.__name__ is "ContributorViewSet":
            return request.method in SAFE_METHODS
        return True

    def has_object_permission(self, request, view, obj):
        if view.__class__.__name__ == "ContributorViewSet":
            return request.method in SAFE_METHODS

        if request.user != obj.author_user:
            return request.method in SAFE_METHODS
