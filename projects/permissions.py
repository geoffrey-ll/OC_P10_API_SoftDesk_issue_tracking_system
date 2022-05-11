from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from rest_framework.permissions import BasePermission, SAFE_METHODS


from .messages_error import MESSAGE_PERMISSION_DENIED
from .models import Project


class ElementAuthorPermission(BasePermission):
    NotAuthenticated(detail="TEST")

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return True
            if view.__class__.__name__ == "ContributorViewSet":
                return \
                    ProjectAuthorPermission.has_permission(self, request, view)
            return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        try:
            return obj.author_user == request.user
        except:
            pass
        try:
            if obj.user:
                if request.user.is_superuser:
                    return True
                return ProjectAuthorPermission.has_object_permission(
                    self, request, view, obj
                )
        except:
            pass
        return False


class ProjectAuthorPermission(BasePermission):
    def has_permission(self, request, view):
        try:
            project = Project.objects.get(id=view.kwargs["project_pk"])
        except:
            raise PermissionDenied(MESSAGE_PERMISSION_DENIED)
        if project.author_user != request.user:
            return request.method in SAFE_METHODS
        return True

    def has_object_permission(self, request, view, obj):
        project = Project.objects.get(id=obj.project.id)
        return project.author_user == request.user


class ProjectContributorPermission(BasePermission):
    # def has_permission(self, request, view):
    #     non défini. Un problème de sécurité ou d'accès ????
    #     À priori n'est appelé que lorsqu'une vue fait un get_queryset,
    #     donc uniquement lorsque has_object_permission est appelé

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if request.user not in [c.user for c in obj]:
            raise PermissionDenied(MESSAGE_PERMISSION_DENIED)
