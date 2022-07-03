from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import SerializerMethodField

from .models import Comment, Contributor, Issue, Project
from .messages_error import MESSAGE_VALIDATED_DATA_IS_NOT_CONTRIBUTOR


def format_datetime(value):
    """Formatage de l'horodatage"""
    return value.strftime("%Y.%m.%d : %T")


def get_url(self):
    """Renvoir l'url de la request"""
    url = self.context['request'].__dict__['_request'].__dict__['META']['PATH_INFO']
    return url


class ContributorSerializer(ModelSerializer):
    """Serializer du model Contributor"""
    MANAGER = 'm', _("Superviseur")
    CONTRIBUTOR = 'c', _("Contributeur")

    user_id = SerializerMethodField("get_user_id")
    endpoint = SerializerMethodField("get_endpoint")

    class Meta:
        model = Contributor
        exclude = ("project", )

    def get_user_id(self, contributor):
        """Renvoi l'{user_id} (différent du {contributor_id})"""
        return contributor.user.id

    def get_endpoint(self, instance):
        """Endpoints"""
        try:
            if self.context["view"].detail is True:
                return ''
            return f"{get_url(self)}{instance.id}"
        except:
            return ''

    def to_representation(self, instance):
        """Représentation front des données"""
        ret = super().to_representation(instance)
        if ret["role"] == self.MANAGER[0]:
            ret["role"] = self.MANAGER[1]
        elif ret["role"] == self.CONTRIBUTOR[0]:
            ret["role"] = self.CONTRIBUTOR[1]
        user = User.objects.get(id=ret["user"])
        ret["user"] = user.username
        return ret


class CommentSerializer(ModelSerializer):
    """Serializer du model Comment"""
    endpoint = SerializerMethodField("get_endpoint")

    class Meta:
        model = Comment
        exclude = ("issue", "author_user", )

    def get_endpoint(self, instance):
        """Endpoints"""
        if self.context["view"].detail is True:
            return ''
        return f"{get_url(self)}{instance.id}"

    def to_representation(self, instance):
        """Représentation front des données"""
        ret = super().to_representation(instance)
        author_user = User.objects.get(username=instance.author_user)
        ret["author_user"] = author_user.username
        ret["created_time"] = format_datetime(instance.created_time)
        return ret


class IssueSerializer(ModelSerializer):
    """Serializer du model Issue"""
    BUG = 'b', _("Bug")
    TASK = 't', _("Tâche")
    ENHANCEMENT = 'e', _("Amélioration")

    LOW = 'l', _("Faible")
    AVERAGE = 'a', _("Moyenne")
    HIGH = 'h', _("Élevé")

    TO_DO = 't', _("À faire")
    IN_PROGRESS = 'i', _("En cours")
    COMPLETED = 'c', _("Terminé")

    endpoint = SerializerMethodField("get_endpoint")

    class Meta:
        model = Issue
        exclude = ("project", "author_user", )

    def get_endpoint(self, instance):
        """Endpoints"""
        if self.context["view"].detail is True:
            return f"{get_url(self)}comments"
        return f"{get_url(self)}{instance.id}"

    def to_representation(self, instance):
        """Repéresentation front des données"""
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

    # def validate_assignee_user(self, value, instance):
    #     """
    #     Vérification que l'utilisateur assigné à une issue est bien
    #     contributor du project
    #     """
    #     print(f"\n{value}\n")
    #     print(f"\n{get_url(self)[14]}\n")
    #     print(f"\n{self}\n")
    #     print(f"\nINSTANCE\n{instance}\n")
    #     # project = instance.project
    #     #
    #     # contributors_user = [c.user for c in project.contributors.all()]
    #     # if value not in contributors_user:
    #     #     raise ValidationError(MESSAGE_VALIDATED_DATA_IS_NOT_CONTRIBUTOR)
    #     return value



class ProjectSerializer(ModelSerializer):
    """Serializer du model Project pour la vue list"""
    BACK_END = 'b', _("Back-end")
    FRONT_END = 'f', _("Front-end")
    IOS = 'i', _("iOS")
    ANDROID = 'a', _("Android")

    manager = SerializerMethodField("get_project_manager")
    my_role = SerializerMethodField("get_contributor__role")
    endpoint = SerializerMethodField("get_endpoint")

    class Meta:
        model = Project
        exclude = ("author_user", )

    @staticmethod
    def get_project_manager(instance):
        """Renvoi le manager du project"""
        queryset = Contributor.objects.get(project=instance, role='m')
        serializers = ContributorSerializer(queryset)
        return serializers.data["user"]

    def get_contributor__role(self, instance):
        """Renvoi le rôle de l'utilisateur"""
        if self.context["request"].user.is_superuser:
            return "Domain supervisor"
        request_user = self.context["request"].user
        queryset = instance.contributors.get(
            project=instance.id,
            user=request_user
        )
        serializer = ContributorSerializer(queryset)
        return serializer.data["role"]

    def get_endpoint(self, instance):
        """Endpoints"""
        if self.context["view"].detail is True:
            return {
                "users": f"{get_url(self)}users",
                "issues": f"{get_url(self)}issues"
            }
        return f"{get_url(self)}{instance.id}"

    def to_representation(self, instance):
        """Représentation front des données"""
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
