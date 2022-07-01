from django.contrib import admin

from .models import Comment, Contributor, Issue, Project


# Register your models here.
def shorting_description(obj):
    """Tronquage de la description pour son affichage"""
    return obj.description[:50]


def shorting_title(obj):
    """Tronquage du titre pour son affichage"""
    return obj.title[:20]


class CommentAdmin(admin.ModelAdmin):
    """
    Représentation des objects comment dans l'administration django
    via navigateur
    """
    list_display = (
        "id", "author_user", "project", "issue", "shorten_description"
    )

    @staticmethod
    def shorten_description(obj):
        """Renvoi la description tronquée"""
        return shorting_description(obj)

    @staticmethod
    def project(obj):
        """Renvoi le project auquel est rattaché le comment"""
        return obj.issue.project


class ContributorAdmin(admin.ModelAdmin):
    """
    Représentation des objects contributor dans l'administration django
    via navigateur
    """
    list_display = ("id", "user", "project", "role")


class IssueAdmin(admin.ModelAdmin):
    """
    Représentation des objects issue dans l'administration django
    via navigateur
    """
    list_display = (
        "id",
        "author_user",
        "assignee_user",
        "project",
        "shorten_title",
        "tag",
        "priority",
        "status"
    )

    @staticmethod
    def shorten_title(obj):
        """Renvoi le titre tronqué"""
        return shorting_title(obj)


class ProjectAdmin(admin.ModelAdmin):
    """
    Représentation des objects project dans l'administration django
    via navigateur
    """
    list_display = ("id", "shorten_title", "type", "author_user")

    @staticmethod
    def shorten_title(obj):
        """Renvoi le titre tronqué"""
        return shorting_title(obj)


admin.site.register(Comment, CommentAdmin)
admin.site.register(Contributor, ContributorAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Project, ProjectAdmin)
