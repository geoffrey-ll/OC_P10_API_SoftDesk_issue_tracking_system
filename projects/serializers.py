from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import SerializerMethodField


from projects.models import Comment, Contributor, Issue, Project
from users.models import User


def format_datetime(value):
    return value.strftime("%Y.%m.%d : %T")


class ContributorListSerializer(ModelSerializer):
    MANAGER = 'm', _("Superviseur")
    CONTRIBUTOR = 'c', _("Contributeur")

    class Meta:
        model = Contributor
        exclude = ("project", )

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if ret["role"] == self.MANAGER[0]:
            ret["role"] = self.MANAGER[1]
        elif ret["role"] == self.CONTRIBUTOR[0]:
            ret["role"] = self.CONTRIBUTOR[1]
        user = User.objects.get(id=ret["user"])
        ret["user"] = user.username
        return ret


class CommentListSerializer(ModelSerializer):
    class Meta:
        model = Comment
        exclude = ("issue", "author_user", )

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        author_user = User.objects.get(username=instance.author_user)
        ret["author_user"] = author_user.username
        ret["created_time"] = format_datetime(instance.created_time)
        return ret


class IssueListSerializer(ModelSerializer):
    BUG  = 'b', _("Bug")
    TASK = 't', _("Tâche")
    ENHANCEMENT = 'e', _("Amélioration")

    LOW = 'l', _("Faible")
    AVERAGE = 'a', _("Moyenne")
    HIGH = 'h', _("Élevé")

    TO_DO = 't', _("À faire")
    IN_PROGRESS = 'i', _("En cours")
    COMPLETED = 'c', _("Terminé")

    class Meta:
        model = Issue
        exclude = ("project", "author_user", )

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if ret["tag"] == self.BUG[0]:
            ret["tag"] = self.BUG[1]
        elif ret["tag"] == self.TASK[0]:
            ret["tag"] = self.TASK[1]
        elif ret["tag"] == self.ENHANCEMENT[0]:
            ret["tag"] = self.ENHANCEMENT[1]

        if ret["priority"] == self.LOW[0]:
            ret["priority"] = self.LOW[1]
        elif ret["priority"] == self.AVERAGE[0]:
            ret["priority"] = self.AVERAGE[1]
        elif ret["priority"] == self.HIGH[0]:
            ret["priority"] = self.HIGH[1]

        if ret["status"] == self.TO_DO[0]:
            ret["status"] = self.TO_DO[1]
        elif ret["status"] == self.IN_PROGRESS[0]:
            ret["status"] = self.IN_PROGRESS[1]
        elif ret["status"] == self.COMPLETED[0]:
            ret["status"] = self.COMPLETED[1]

        assignee_user = User.objects.get(id=ret["assignee_user"])
        author_user = User.objects.get(username=instance.author_user)
        ret["assignee_user"] = assignee_user.username
        ret["author_user"] = author_user.username

        ret["created_time"] = format_datetime(instance.created_time)

        return ret


class ProjectListSerializer(ModelSerializer):
    BACK_END = 'b', _("Back-end")
    FRONT_END = 'f', _("Front-end")
    IOS = 'i', _("iOS")
    ANDROID = 'a', _("Android")

    class Meta:
        model = Project
        exclude = ("author_user", )

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if ret["type"] == self.BACK_END[0]:
            ret["type"] = self.BACK_END[1]
        elif ret["type"] == self.FRONT_END[0]:
            ret["type"] = self.FRONT_END[1]
        elif ret["type"] == self.IOS[0]:
            ret["type"] = self.IOS[1]
        elif ret["type"] == self.ANDROID[0]:
            ret["type"] = self.ANDROID[1]
        return ret


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
