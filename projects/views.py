from rest_framework.exceptions import NotAcceptable, NotAuthenticated, \
    NotFound, PermissionDenied
# from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, ViewSet


from projects.models import Comment, Contributor, Issue, Project
from projects.serializers import ContributorListSerializer, \
    CommentListSerializer, IssueListSerializer, ProjectListSerializer
# from projects.permissions import AuthorPermission,


# Create your views here.
MESSAGE_NOT_AUTHENTICATED = "Cette API nécessite d'être authentifié."
MESSAGE_NOT_FOUND = "Projet inexistant."
MESSAGE_PERMISSION_DENIED = "Vous n'êtes pas contributeur de ce project."


# class GetQuerysetMixin:
#     def get_queryset(self):
#         project = self.kwargs["project_pk"]
#         contributors_project = Contributor.objects.filter(project=project)
#         if self.request.user in [c.user for c in contributors_project]:
#             return Issue.objects.filter(project=project)
#         else:
#             raise PermissionDenied(
#                 "Vous n'êtes pas contributeur de ce project."
#             )


def get_queryset_mixin(self):
    project = self.kwargs["project_pk"]
    contributors_project = Contributor.objects.filter(project=project)
    if self.request.user in [c.user for c in contributors_project]:
        return project, contributors_project
    else:
        raise PermissionDenied(MESSAGE_PERMISSION_DENIED)


class ContributorViewSet(ModelViewSet):
    serializer_class = ContributorListSerializer

    def get_queryset(self):
        contributors_project = get_queryset_mixin(self)[1]
        return contributors_project

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            project = Project.objects.get(id=self.kwargs["project_pk"])
            try:
                return serializer.save(project=project)
            except:
                raise NotAcceptable(
                    "Un seul superviseur par project. "
                    "Ce project a déjà un superviseur."
                )


class CommentViewSet(ModelViewSet):
    serializer_class = CommentListSerializer

    def get_queryset(self):
        get_queryset_mixin(self)
        return Comment.objects.filter(issue=self.kwargs["issue_pk"])

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            issue = Issue.objects.get(id=self.kwargs["issue_pk"])
            return serializer.save(issue=issue, author_user=self.request.user)


class IssueViewSet(ModelViewSet):
    serializer_class = IssueListSerializer

    def get_queryset(self):
        project = get_queryset_mixin(self)[0]
        return Issue.objects.filter(project=project)

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            project = Project.objects.get(id=self.kwargs["project_pk"])
            contributors_user = [c.user for c in project.contributors.all()]
            assigned_user = serializer.validated_data['assignee_user']

            if assigned_user not in contributors_user:
                raise NotAcceptable(
                    "L'utilisateur n'est pas contributeur à ce project."
                )
            return serializer.save(
                project=project, author_user=self.request.user
            )


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectListSerializer

    def get_queryset(self):
        user_contributions = Contributor.objects.filter(user=self.request.user)
        # projects_user = [c.project.id for c in user_contributions]
        # return Project.objects.filter(id__in=projects_user)
        return Project.objects.filter(contributors__in=user_contributions)

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            try:
                instance = serializer.save(author_user=self.request.user)
                Contributor.objects.create(
                    user=self.request.user, project=instance, role='m'
                )
                return
            except:
                raise NotAcceptable(
                    "Plusieurs projects de même type ne peuvent pas partagés "
                    "le même nom."
                )
