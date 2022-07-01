from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet

from .models import Comment, Contributor, Issue, Project
from .serializers import (
    ContributorSerializer,
    CommentSerializer,
    IssueSerializer,
    ProjectSerializer
)
from .messages_error import (
    MESSAGE_VALIDATED_DATA_IS_NOT_CONTRIBUTOR,
    MESSAGE_VALIDATED_DATA_NOT_MANY_MANAGER,
    MESSAGE_VALIDATED_DATA_TITLE_PROJECT
)


def get_project_pk(self):
    """Renvoi le pk d'un project depuis l'url de la request"""
    return self.kwargs["project_pk"]


def get_contributors_project(self):
    """Renvoi le queryset des contributeurs d'un project depuis son pk"""
    return Contributor.objects.filter(project=get_project_pk(self))


class ContributorViewSet(ModelViewSet):
    """ViewSet de Contributor"""
    serializer_class = ContributorSerializer

    def get_queryset(self):
        """Renvoi un queryset"""
        return get_contributors_project(self)

    def perform_create(self, serializer):
        """
        Pour associer le project lors de l'ajout d'un nouveau contributeur
        dans le project
        """
        if self.request.user.is_authenticated:
            project = Project.objects.get(id=get_project_pk(self))
            try:
                return serializer.save(project=project)
            except:
                raise ValidationError(MESSAGE_VALIDATED_DATA_NOT_MANY_MANAGER)


class CommentViewSet(ModelViewSet):
    """ViewSet de Comment"""
    serializer_class = CommentSerializer

    def get_queryset(self):
        """Renvoi un queryset"""
        return Comment.objects.filter(issue=self.kwargs["issue_pk"])

    def perform_create(self, serializer):
        """
        Pour associer l'issue lors de l'ajout d'un nouveau comment
        dans le l'issue
        """
        if self.request.user.is_authenticated:
            issue = Issue.objects.get(id=self.kwargs["issue_pk"])
            return serializer.save(issue=issue, author_user=self.request.user)


class IssueViewSet(ModelViewSet):
    """ViewSet de Issue"""
    serializer_class = IssueSerializer

    def get_queryset(self):
        """Renvoi un queryset"""
        return Issue.objects.filter(project=get_project_pk(self))

    def perform_create(self, serializer):
        """
        Vérifie que l'user assigné à l'issue est contributeur du project
        avant d'enregistrer la nouvelle issue
        """
        if self.request.user.is_authenticated:
            project = Project.objects.get(id=get_project_pk(self))
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
    """ViewSet de Project"""
    serializer_class = ProjectSerializer

    def get_queryset(self):
        """Renvoi un queryset"""
        if self.request.user.is_superuser:
            return Project.objects.all()
        else:
            user_contributions = Contributor.objects.filter(
                user=self.request.user
            )
            return Project.objects.filter(contributors__in=user_contributions)

    def perform_create(self, serializer):
        """
        Pour attribuer le rôle de manager à l'user lors de l'ajout
        d'un nouveau project
        """
        if self.request.user.is_authenticated:
            try:
                instance = serializer.save(author_user=self.request.user)
                Contributor.objects.create(
                    user=self.request.user, project=instance, role='m'
                )
                return
            except:
                raise ValidationError(MESSAGE_VALIDATED_DATA_TITLE_PROJECT)
