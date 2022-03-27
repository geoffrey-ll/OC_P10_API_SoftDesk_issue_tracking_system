from django.db import models
from django.utils.translation import gettext_lazy as _


from users.models import User


# Create your models here.
class Project:
    class ProjectType(models.TextChoices):
        BACK_END = "b", _("Back-end")
        FRONT_END = "f", _("Front-end")
        IOS = 'i', _("iOS")
        ANDROID = 'a', _("Android")

    # project_id = models.IntegerField()   # Nécessaire ?? id déjà par défault
    title = models.CharField(max_lengt=100)
    description = models.CharField(max_length=5_000)
    type = models.CharField(choices=ProjectType.choices,
                            default=ProjectType.BACK_END)
    author_user = models.ForeignKey(to=Contributor, on_delete=models.CASCADE)


class Contributor:
    class ContributorRole(models.TextChoices):
        MANAGER = 'm', _("Superviseur")
        CONTRIBUTOR = 'c', _("Contributeur")

    # IntegerField dans le word…
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    # IntegerField dans le word…
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    # ChoiceField n'existe pas ……
    # permission = models.ChoiceField()
    role = models.CharField(choices=ContributorRole.choices,
                            default=ContributorRole.CONTRIBUTOR)

    class Meta:
        """Unicité d'un contributor."""
        unique_together = ("user", "project")


class Issue:
    class IssueTag(models.TextChoices):
        BUG = 'b', _("Bug")
        TASK = 't', _("Tâche")
        ENHANCEMENT = 'e', _("Amélioration")

    class IssuePriority(models.TextChoices):
        WEAK = 'w', _("Faible")
        AVERAGE = 'a', _("Moyenne")
        HIGH = 'h', _("Haute")

    class IssueStatus(models.TextChoices):
        TO_DO = 't', _("À faire")
        IN_PROGRESS = 'i', _("En cours")
        COMPLETED = 'c', _("Terminé")

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=5_000)
    tag = models.CharField(choices=IssueTag.choices, default=IssueTag.TASK)
    priority = models.CharField(choices=IssuePriority,
                                default=IssuePriority.AVERAGE)
    # IntegerField dans le word…
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    status = models.CharField(choices=IssueStatus, default=IssueStatus.TO_DO)
    author_user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    assignee_user = models.ForeignKey(to=User, default=author_user,
                                      on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)


class Comment:
    # comment_id = models.IntegerField()   # Nécessaire ?? id déjà par défault
    description = models.CharField(max_lenght=5_000)
    author_user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    issue = models.ForeignKey(to=Issue, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("issue", "author_user")
