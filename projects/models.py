from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q, UniqueConstraint

from .translates import (
    ContributorRole, IssuePriority, IssueStatus, IssueTag, ProjectType
)


# Create your models here.
class Project(models.Model):
    """Model project"""
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    type = models.CharField(
        max_length=1, choices=ProjectType.choices, default=ProjectType.BACK_END
    )
    author_user = models.ForeignKey(to=User, on_delete=models.CASCADE)

    class Meta:
        """Règle d'unicité des project"""
        unique_together = ("id", "author_user")
        constraints = [
            UniqueConstraint(
                fields=["title", "type"],
                name="unique_project_type"
            )
        ]

    def __str__(self):
        """Repéresentation de l'object project"""
        return f"{self.id} : {self.title[:20]}"


class Contributor(models.Model):
    """Model contributor"""
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    project = models.ForeignKey(
        to=Project, on_delete=models.CASCADE, related_name="contributors"
    )
    role = models.CharField(
        max_length=1,
        choices=ContributorRole.choices,
        default=ContributorRole.CONTRIBUTOR
    )

    class Meta:
        """Règle d'unicité des contributor"""
        unique_together = ("user", "project")
        constraints = [
            UniqueConstraint(
                fields=["project"],
                condition=Q(role='m'),
                name="unique_project_manager"
            )
        ]


class Issue(models.Model):
    """Model issue"""
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    tag = models.CharField(
        max_length=1, choices=IssueTag.choices, default=IssueTag.TASK
    )
    priority = models.CharField(
        max_length=1,
        choices=IssuePriority.choices,
        default=IssuePriority.AVERAGE
    )
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=1, choices=IssueStatus.choices, default=IssueStatus.TO_DO
    )
    author_user = models.ForeignKey(
        to=User, related_name="created_issues", on_delete=models.CASCADE
    )
    assignee_user = models.ForeignKey(
        to=User,
        related_name="assigned_issues",
        default=author_user,
        on_delete=models.CASCADE
    )
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Repéresentation de l'object issue"""
        return f"{self.id} : {self.title[:20]}"


class Comment(models.Model):
    """Model comment"""
    issue = models.ForeignKey(to=Issue, on_delete=models.CASCADE)
    author_user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    description = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
