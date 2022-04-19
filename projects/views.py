from rest_framework.exceptions import NotAcceptable
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, ViewSet


from projects.models import Comment, Contributor, Issue, Project
from projects.serializers import ContributorListSerializer, \
    CommentListSerializer, IssueListSerializer, ProjectListSerializer


# Create your views here.
class ContributorViewSet(ModelViewSet):
    serializer_class = ContributorListSerializer

    def get_queryset(self):
        return Contributor.objects.filter(project=self.kwargs["project_pk"])

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            project = Project.objects.get(id=self.kwargs["project_pk"])
            try:
                return serializer.save(project=project)
            except:
                raise NotAcceptable(
                    "Un seul superviseur par project "
                    "Ce project a déjà un superviseur."
                )


class CommentViewSet(ModelViewSet):
    serializer_class = CommentListSerializer

    def get_queryset(self):
        return Comment.objects.filter(issue=self.kwargs["issue_pk"])

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            issue = Issue.objects.get(id=self.kwargs["issue_pk"])
            return serializer.save(issue=issue, author_user=self.request.user)


class IssueViewSet(ModelViewSet):
    serializer_class = IssueListSerializer

    def get_queryset(self):
        return Issue.objects.filter(project=self.kwargs["project_pk"])

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            project = Project.objects.get(id=self.kwargs["project_pk"])
            return serializer.save(
                project=project, author_user=self.request.user
            )


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectListSerializer

    def get_queryset(self):
        contributors_user = Contributor.objects.filter(user=self.request.user)
        projects_user = [c.project.id for c in contributors_user]
        return Project.objects.filter(id__in=projects_user)

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            instance = serializer.save(author_user=self.request.user)
            Contributor.objects.create(
                user=self.request.user, project=instance, role='m'
            )
            return
