from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import SerializerMethodField


from projects.models import Comment, Contributor, Issue, Project


class ProjectListSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "title", "author_user", "type"]



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
#
# class ContributorListSerializer(ModelSerializer):
#     class Meta:
#         model = Contributor
#         field = ["id", "user", "role"]
