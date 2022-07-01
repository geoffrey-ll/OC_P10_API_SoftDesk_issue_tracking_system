from django.utils.translation import gettext_lazy as _
from django.db import models


class ContributorRole(models.TextChoices):
    """Choix des rôles possible au sein d'un project"""
    MANAGER = 'm', _("Superviseur")
    CONTRIBUTOR = 'c', _("Contributeur")


class ProjectType(models.TextChoices):
    """Choix des types de project possibles"""
    BACK_END = 'b', _("Back-end")
    FRONT_END = 'f', _("Front-end")
    IOS = 'i', _("iOS")
    ANDROID = 'a', _("Android")


class IssueTag(models.TextChoices):
    """Choix des types d'issues possibles"""
    BUG = 'b', _("Bug")
    TASK = 't', _("Tâche")
    ENHANCEMENT = 'e', _("Amélioration")


class IssuePriority(models.TextChoices):
    """Choix des prioritées d'issues possibles"""
    LOW = 'l', _("Faible")
    AVERAGE = 'a', _("Moyenne")
    HIGH = 'h', _("Haute")


class IssueStatus(models.TextChoices):
    """Choix des status d'issues possibles"""
    TO_DO = 't', _("À faire")
    IN_PROGRESS = 'i', _("En cours")
    COMPLETED = 'c', _("Terminé")
