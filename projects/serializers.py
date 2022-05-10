from django.contrib.auth.models import User
from django.db import models
from django.forms.models import model_to_dict
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import SerializerMethodField


from projects.models import Comment, Contributor, Issue, Project
from .translates import ContributorRole, \
    IssuePriority, IssueStatus, IssueTag, \
    ProjectType
from .translates import translating_database


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


# def translating_database(fields_to_translate, ret):
#     for field, translator in fields_to_translate:
#         from .translates import f"{translator}
#         for var in translator:
#             if ret[field] == var[0]:
#                 return var[1]
#         return None
#     pass


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

    manager = SerializerMethodField("get_project_manager")
    my_role = SerializerMethodField("get_contributor__role")
    url_project = SerializerMethodField("get_url_project")

    class Meta:
        model = Project
        exclude = ("author_user", )

    def get_project_manager(self, instance):
        queryset = Contributor.objects.get(project=instance, role='m')
        serializers = ContributorListSerializer(queryset)
        return serializers.data["user"]

    def get_contributor__role(self, instance):
        if self.context["request"].user.is_superuser:
            return
        request_user = self.context["request"].user
        queryset = instance.contributors.get(
            project=instance.id,
            user=request_user
        )
        serializer = ContributorListSerializer(queryset)
        return serializer.data["role"]

    def get_url_project(self, instance):
        return f"localhost:8000/api/projects/{instance.id}"

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
