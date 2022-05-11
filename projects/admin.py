from django.contrib import admin


from .models import Comment, Contributor, Issue, Project


# Register your models here.
def shorting_title(obj):
    return obj.title[:20]


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "id", "author_user", "project", "issue", "shorten_description"
    )

    def shorten_description(self, obj):
        return obj.description[:50]

    def project(self, obj):
        return obj.issue.project


class ContributorAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "project", "role")


class IssueAdmin(admin.ModelAdmin):
    list_display = ("id", "author_user", "assignee_user", "project",
                    "shorten_title", "tag", "priority", "status")

    def shorten_title(self, obj):  # Rennomer title ?? view_title ??
        return shorting_title(obj)


class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "shorten_title", "type", "author_user")

    def shorten_title(self, obj):  # Rennomer title ?? view_title ??
        return shorting_title(obj)


admin.site.register(Comment, CommentAdmin)
admin.site.register(Contributor, ContributorAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Project, ProjectAdmin)
