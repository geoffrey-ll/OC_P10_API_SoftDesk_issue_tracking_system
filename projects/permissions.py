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
        # view.queryset
        test01 = view.__getqueryset__
        print(f"\ntest01\n{test01}\n")
        test02 = view.__getqueryset__.author_user
        print(f"\ntest02\n{test02}\n")

        return Contributor.objects.get(
            project=view.kwargs["project_pk"],
            user=request.user
        ).role

    def has_permission(self, request, view):
        # option = "has_permission"
        print(f"\nhas 01\n")
        if request.user.is_authenticated:
            print(f"\nhas 02\n")
            # if view.__class__.__name__ == "ProjectViewSet":
            #     return True
            # else:
                # return self.assign_permission(request, view, option)
            if request.user.is_superuser:
                print(f"\nhas 03\n")
                # return superuser_permission(request, view, option="has_perm")
                return SuperuserPermission().has_permission(request, view)
            elif view.__class__.__name__ == "ProjectViewSet":
                print(f"\nhas 04\n")
                return True

            else:
                print(f"\nhas 05\n")
                try:
                    print(f"\nhas 06\n")
                    my_role = self.get_my_role(request, view)
                except:
                    print(f"\nhas except 01\n")
                    raise PermissionDenied(detail=MESSAGE_PERMISSION_DENIED)

                if my_role == 'm':
                    print(f"\nhas 07\n")
                    return ManagerPermission().has_permission(
                        request, view
                    )
                if my_role == 'c':
                    print(f"\nhas 08\n")
                    return ContributorPermission().has_permission(
                        request, view
                    )
        print(f"\nhas except 02\n")
        raise NotAuthenticated(detail=MESSAGE_PERMISSION_NOT_AUTHENTICATED)

    def has_object_permission(self, request, view, obj):
        print(f"\nobj 01\n")
        if request.user.is_authenticated:
            print(f"\nobj 02\n")
            # return self.assign_permission(request, view)
            if request.user.is_superuser:
                print(f"\nobj 03\n")
                # return superuser_permission(request, option="has_obj")
                return SuperuserPermission().has_object_permission(
                    request, view, obj
                )

            else:
                print(f"\nobj 04\n")
                try:
                    print(f"\nobj 05\n")
                    my_role = self.get_my_role(request, view)
                except:
                    print(f"\nobj except 01\n")
                    raise PermissionDenied(detail=MESSAGE_PERMISSION_DENIED)

                if my_role == 'm':
                    print(f"\nobj 06\n")
                    return ManagerPermission().has_object_permission(
                        request, view, obj
                    )
                if my_role == 'c':
                    print(f"\nobj 07\n")
                    return ContributorPermission().has_object_permission(
                        request, view, obj
                    )

        print(f"\nobj except 02\n")
        raise NotAuthenticated(detail=MESSAGE_PERMISSION_NOT_AUTHENTICATED)


# Échec sous forme de def ………
#
# def superuser_permission(request, option):
#     # def has_permission(request, view):
#     if option == "has_perm":
#         print(f"\nLA\n")
#         return request.method in SAFE_METHODS
#
#     # def has_object_permission(request, view, obj):
#     if option == "has_obj":
#         print(f"\nICI\n")
#         return True

class SuperuserPermission(BasePermission):
    SAFE_METHODS = ["GET", "PUT", "DELETE", "HEAD", "OPTION"]

    def has_permission(self, request, view):
        print(f"\nLA\n")
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        print(f"\nICI\n")
        return True


class ManagerPermission(BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if view.__class__.__name__ == "ContributorViewSet" \
                or view.__class__.__name__ == "ProjectViewSet":
            return True
        # else: Inutile ??
        if request.user != obj.author_user:
            return request.method in SAFE_METHODS
        return True


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
        return True
