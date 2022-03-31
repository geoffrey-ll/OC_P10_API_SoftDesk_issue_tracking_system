from django.shortcuts import render
from rest_framework.fields import CurrentUserDefault
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet


from projects.serializers import ProjectListSerializer
from projects.models import Comment, Contributor, Issue, Project


# Create your views here.


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectListSerializer

    def get_queryset(self, request):
        projects_user = Contributor.objects.filter(user=request.user)
        return Project.objects.filter(id__in=projects_user)
