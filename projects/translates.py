from django.utils.translation import gettext_lazy as _
from django.db import models


class ContributorRole(models.TextChoices):
    MANAGER = 'm', _("Superviseur")
    CONTRIBUTOR = 'c', _("Contributeur")


class ProjectType(models.TextChoices):
    BACK_END = 'b', _("Back-end")
    FRONT_END = 'f', _("Front-end")
    IOS = 'i', _("iOS")
    ANDROID = 'a', _("Android")


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


all_vars_contributor_role = [
    ContributorRole.MANAGER,
    ContributorRole.CONTRIBUTOR
]
all_vars_project_type = [
    ProjectType.BACK_END,
    ProjectType.FRONT_END,
    ProjectType.IOS,
    ProjectType.ANDROID
]
all_vars_issue_tag = [
    IssueTag.BUG,
    IssueTag.TASK,
    IssueTag.ENHANCEMENT
]
all_vars_issue_priority = [
    IssuePriority.LOW,
    IssuePriority.AVERAGE,
    IssuePriority.HIGH
]
all_vars_issue_status = [
    IssueStatus.TO_DO,
    IssueStatus.IN_PROGRESS,
    IssueStatus.COMPLETED
]

fields_to_translate_issue = [
    ("tag", all_vars_issue_tag),
    ("priority", all_vars_issue_priority),
    ("status", all_vars_issue_status)
]

def translating_database(serializer, instance):
    if serializer == "issue":
        print(f"\nclass:\n{IssueTag}\n")
        for elmt in IssueTag:
            if instance["tag"] == elmt:
                instance["tag"] = _
        for elmt in IssuePriority:
            if instance["priority"] == elmt:
                instance["priority"] = _

        return instance
    #     for field, translator in fields_to_translate_issue:
    #         for var in translator:
    #             print(f"\ntranslator\n{translator}\n")
    #             print(f"\nvar:\n{var}\n")
    #             # print(f"\nret:\n{ret[field]}\n")
    #             if ret[field] == var:
    #                 ret[field] = var
    #                 return ret
    #         return None
    # pass


# def get_y(a, my_list):
#     for x, y in my_list:
#         if a == x:
#             return y
#     return None