from django.contrib import admin


# from .models import User


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    """Colonnes des informations sur les users présentes dans l'Admin Django"""
    list_display = ["id", "username", "first_name", "last_name", "email",
                    "password"]


admin.site.register(User, UserAdmin)
