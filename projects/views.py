from django.shortcuts import render
from rest_framework.fields import CurrentUserDefault
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, ViewSet
from rest_framework.request import Request
from rest_framework.response import Response


from projects.models import Comment, Contributor, Issue, Project
from projects.serializers import ContributorListSerializer, \
    ProjectListSerializer


# Create your views here.


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectListSerializer

    def get_queryset(self):
        contributors_user = Contributor.objects.filter(user=self.request.user)
        projects_user = [c.project.id for c in contributors_user]
        return Project.objects.filter(id__in=projects_user)


class ContributorViewSet(ModelViewSet):
    serializer_class = ContributorListSerializer

    print(f"\nJE PASSE ICI\n")
    #
    def get_queryset(self):
        print(f"\nJE PASSE LÀ\n")
        # project = Project.objects.get_object()
        print(f"\ntest:\n{self.request.query_params}\n")
        return Contributor.objects.filter(project=1)


# class ContributorViewSet(ViewSet):
#     def list(self, request, projects_pk=None):
#         contributors = self.queryset.filter(project=projects_pk)
#         return Response()
#
#     def retrieve(self, request, pk=None, projects_pk=None):
#         contributors = self.queryset.get(pk=pk, project=projects_pk)
#         return Response(serializer.data)
