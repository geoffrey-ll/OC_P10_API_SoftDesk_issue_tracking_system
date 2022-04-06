from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import SerializerMethodField
from rest_framework.serializers import HyperlinkedModelSerializer
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer


from projects.models import Comment, Contributor, Issue, Project


class ContributorListSerializer(ModelSerializer):
    # Temporaire. Test pour le POST avec drf-Nested
    # parent_lookup_kwargs = {"project_pk": "project__id"}

    class Meta:
        model = Contributor
        fields = ["id", "user", "role"]


class CommentListSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "author_user", "created_time", "description"]


class IssueListSerializer(ModelSerializer):
    class Meta:
        model = Issue
        fields = ["id", "title", "tag", "priority", "status", "author_user",
                  "assignee_user", "created_time", "description"]


class ProjectListSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "title", "author_user", "type", "description"]


# FUTUR :

# class ProjectDetailSerializer(ModelSerializer):
#     contributors = SerializerMethodField
#
#     class Meta:
#         model = Project
#         fields = ["id", "title", "author_user", "type", "description",
#                   "contributors"]
#
#     def get_contributors(self, instance):
#         queryset = instance.contributors.filter(project=self.id)
#         serializer = ContributorListSerializer(queryset, many=True)
#         return serializer.data
#
