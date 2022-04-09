from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import SerializerMethodField


from projects.models import Comment, Contributor, Issue, Project


class ContributorListSerializer(ModelSerializer):
    class Meta:
        model = Contributor
        exclude = ("project", )


class CommentListSerializer(ModelSerializer):
    class Meta:
        model = Comment
        exclude = ("issue", "author_user", )


class IssueListSerializer(ModelSerializer):
    class Meta:
        model = Issue
        exclude = ("project", "author_user", )


class ProjectListSerializer(ModelSerializer):
    class Meta:
        model = Project
        exclude = ("author_user", )



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
