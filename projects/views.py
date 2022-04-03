from django.shortcuts import render
from rest_framework.fields import CurrentUserDefault
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
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

    def get_queryset(self):
        print(f"\nJE PASSE LÀ\n")
        print(f"\nGET:\n{self.request.GET.get('project_title')}\n")
        return Contributor.objects.filter(project=self.request.GET.get("project_id"))
