from rest_framework.exceptions import NotAcceptable, NotAuthenticated, \
    NotFound, PermissionDenied, ValidationError
# from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, ViewSet


from projects.models import Comment, Contributor, Issue, Project
from projects.serializers import ContributorListSerializer, \
    CommentListSerializer, IssueListSerializer, ProjectListSerializer
# from projects.permissions import AuthorPermission,

from .messages_error import MESSAGE_VALIDATED_DATA_IS_NOT_CONTRIBUTOR, \
    MESSAGE_VALIDATED_DATA_NOT_MANY_MANAGER, \
    MESSAGE_VALIDATED_DATA_TITLE_PROJECT
# from .permissions import ProjectContributorPermission, TestPermission, ElementAuthorPermission


# Create your views here.


# class GetQuerysetMixin:   OU GetDataMixin
#   def get_project(self, view):
#       return view.kwargs["project_pk"]
#
#   def get_contributors_project(self):
#       return Contributor.objects.filter(project=self.get_project)

# EXEMPLE:
# def get_queryset(self):
#     contributors_project = GetQuerysetMixin.contributors_project(self)



def get_queryset_mixin(self):
    project = self.kwargs["project_pk"]
    contributors_project = Contributor.objects.filter(project=project)
    # ProjectContributorPermission.has_object_permission(
    #     self, self.request, self, contributors_project
    # )
    return project, contributors_project


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
                raise ValidationError(MESSAGE_VALIDATED_DATA_NOT_MANY_MANAGER)


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
                raise ValidationError(
                    MESSAGE_VALIDATED_DATA_IS_NOT_CONTRIBUTOR
                )
            return serializer.save(
                project=project, author_user=self.request.user
            )


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectListSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Project.objects.all()
        else:
            user_contributions = Contributor.objects.filter(
                user=self.request.user
            )
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
                raise ValidationError(MESSAGE_VALIDATED_DATA_TITLE_PROJECT)
