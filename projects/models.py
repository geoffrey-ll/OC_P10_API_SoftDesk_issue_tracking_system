# from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


from users.models import User


# Create your models here.
class Project(models.Model):
    class ProjectType(models.TextChoices):
        BACK_END = "b", _("Back-end")
        FRONT_END = "f", _("Front-end")
        IOS = 'i', _("iOS")
        ANDROID = 'a', _("Android")

    # project_id = models.IntegerField(unique=True)  # À rajouter si besoin.
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=1, choices=ProjectType.choices,
                            default=ProjectType.BACK_END)
    author_user = models.ForeignKey(to=User, on_delete=models.CASCADE)

    # Ajouter fonction pour généner automatiquement un contributor avec le
    # rôle de superviseur, pour le author_user de Project

    class Meta:
        unique_together = ("id", "author_user")

    def __str__(self):
        return f"{self.id} : {self.title[:20]}"


class Contributor(models.Model):
    class ContributorRole(models.TextChoices):
        MANAGER = 'm', _("Superviseur")
        CONTRIBUTOR = 'c', _("Contributeur")

    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    # permission = models.ChoiceField()
    role = models.CharField(max_length=1, choices=ContributorRole.choices,
                            default=ContributorRole.CONTRIBUTOR)

    class Meta:
        """Unicité d'un contributor."""
        unique_together = ("user", "project")


class Issue(models.Model):
    class IssueTag(models.TextChoices):
        BUG = 'b', _("Bug")
        TASK = 't', _("Tâche")
        ENHANCEMENT = 'e', _("Amélioration")

    class IssuePriority(models.TextChoices):
        LOW = 'l', _("Faible")
        AVERAGE = 'a', _("Moyenne")
        HIGH = 'h', _("Haute")

    class IssueStatus(models.TextChoices):
        TO_DO = 't', _("À faire")
        IN_PROGRESS = 'i', _("En cours")
        COMPLETED = 'c', _("Terminé")

    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    tag = models.CharField(max_length=1, choices=IssueTag.choices,
                           default=IssueTag.TASK)
    priority = models.CharField(max_length=1, choices=IssuePriority.choices,
                                default=IssuePriority.AVERAGE)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=IssueStatus.choices,
                              default=IssueStatus.TO_DO)
    author_user = models.ForeignKey(to=User, related_name="created_issues",
                                    on_delete=models.CASCADE)
    assignee_user = models.ForeignKey(to=User, related_name="assigned_issues",
                                      default=author_user,
                                      on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} : {self.title[:20]}"


class Comment(models.Model):
    description = models.TextField(null=True, blank=True)
    author_user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    issue = models.ForeignKey(to=Issue, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
