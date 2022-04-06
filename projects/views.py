from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, ViewSet


from projects.models import Comment, Contributor, Issue, Project
from projects.serializers import ContributorListSerializer, \
    CommentListSerializer, IssueListSerializer, ProjectListSerializer


# Create your views here.
class ContributorViewSet(ModelViewSet):
    serializer_class = ContributorListSerializer

    def get_queryset(self):
        return Contributor.objects.filter(project=self.kwargs["project_pk"])

    def create(self, request, *args, **kwargs):
        project = Project.objects.get(id=self.kwargs["project_pk"])
        project_id = self.kwargs["project_pk"]
        request.data._mutable = True
        request.data["project"] = project_id
        request.data._mutable = False
        print(f"\ntest id :\n{project_id}\n")
        print(f"\ntest:\n{request.data}\n")
        return HttpResponse(request)
        # return HttpResponse(self, request, *args, **kwargs)

    # def retrieve(self, request, pk=None, project_pk=None):
    #     queryset = Contributor.object.filter(project=project_pk)
    #     contributors = get_object_or_404(queryset)
    #     serializer = ContributorListSerializer(contributors)
    #     return Response(serializer.data)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentListSerializer

    def get_queryset(self):
        return Comment.objects.filter(issue=self.kwargs["issue_pk"])


class IssueViewSet(ModelViewSet):
    serializer_class = IssueListSerializer

    def get_queryset(self):
        return Issue.objects.filter(project=self.kwargs["project_pk"])


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectListSerializer

    def get_queryset(self):
        contributors_user = Contributor.objects.filter(user=self.request.user)
        projects_user = [c.project.id for c in contributors_user]
        return Project.objects.filter(id__in=projects_user)
