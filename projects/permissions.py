from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from rest_framework.permissions import BasePermission, SAFE_METHODS


from .messages_error import MESSAGE_PERMISSION_DENIED, MESSAGE_PERMISSION_NOT_AUTHENTICATED
from .models import Contributor, Project

# ANCIEN CODE DES PERMISSIONS

# class ElementAuthorPermission(BasePermission):
#     def has_permission(self, request, view):
#         if request.user.is_authenticated:
#             if request.user.is_superuser:
#                 return True
#                 # if request.method not in SAFE_METHODS:
#                 #     return False
#             if view.__class__.__name__ == "ContributorViewSet":
#                 return \
#                     ProjectAuthorPermission.has_permission(self, request, view)
#             return True
#
#     def has_object_permission(self, request, view, obj):
#         if request.method in SAFE_METHODS:
#             return True
#         try:
#             return obj.author_user == request.user
#         except:
#             pass
#         try:
#             if obj.user:
#                 if request.user.is_superuser:
#                     if request.method is "PUT":
#                         return True
#                     return True
#                 return ProjectAuthorPermission.has_object_permission(
#                     self, request, view, obj
#                 )
#         except:
#             pass
#         return False
#
#
# class ProjectAuthorPermission(BasePermission):
#     def has_permission(self, request, view):
#         try:
#             project = Project.objects.get(id=view.kwargs["project_pk"])
#         except:
#             raise PermissionDenied(MESSAGE_PERMISSION_DENIED)
#         if project.author_user != request.user:
#             return request.method in SAFE_METHODS
#         return True
#
#     def has_object_permission(self, request, view, obj):
#         project = Project.objects.get(id=obj.project.id)
#         return project.author_user == request.user
#
#
# class ProjectContributorPermission(BasePermission):
#     # def has_permission(self, request, view):
#     #     non défini. Un problème de sécurité ou d'accès ????
#     #     À priori n'est appelé que lorsqu'une vue fait un get_queryset,
#     #     donc uniquement lorsque has_object_permission est appelé
#
#     def has_object_permission(self, request, view, obj):
#         if request.user.is_superuser:
#             return True
#         if request.user not in [c.user for c in obj]:
#             raise PermissionDenied(MESSAGE_PERMISSION_DENIED)
#
#
# class TestPermission(BasePermission):
#     def has_permission(self, request, view):
#         return True
#     def has_object_permission(self, request, view, obj):
#         return True
#____________________________________



# NOUVEAU CODE DES PERMISSIONS

class DefaultPermission(BasePermission):
    # Échec factorisation des éléments communs aux has_perm et has_obj
    #
    # def assign_permission(self, request, view, option):
    #     if request.user.is_superuser:
    #         if option == "has_permission":
    #             return SuperuserPermission().has_permission(request, view)
    #         else:
    #             return SuperuserPermission().has_object_permission(
    #                 request, view, obj
    #             )
    #     else:
    #         # project = Project.objects.get(id=view.kwargs["project_pk"])
    #         my_role = Contributor.objects.get(
    #             project=view.kwargs["project_pk"],
    #             user=request.user
    #         )
    #         if my_role == 'm':
    #             return ManagerPermission()
    #         if my_role == 'c':
    #             return ContributorPermission()
    #_____________________

    def get_my_role(self, request, view):
        if view.__class__.__name__ == "ProjectViewSet":
            project_id = view.kwargs["pk"]
        else:
            project_id = view.kwargs["project_pk"]

        print(f"\n{Contributor.objects.exist(project=project_id, user=request.user)}\n")

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
        print(f"\nMANAGER   HAS")
        return True

    def has_object_permission(self, request, view, obj):
        print(f"\nMANAGER   OBJ")
        if view.__class__.__name__ == "ContributorViewSet" \
                or view.__class__.__name__ == "ProjectViewSet":
            return True
        if request.user != obj.author_user:
            return request.method in SAFE_METHODS


class ContributorPermission(BasePermission):
    def has_permission(self, request, view):
        print(f"\nCONTRIBUTEUR   HAS")
        if view.__class__.__name__ is "ContributorViewSet":
            return request.method in SAFE_METHODS
        return True

    def has_object_permission(self, request, view, obj):
        print(f"\nCONTRIBUTEUR   OBJ")
        if view.__class__.__name__ == "ContributorViewSet":
            return request.method in SAFE_METHODS

        if request.user != obj.author_user:
            return request.method in SAFE_METHODS
