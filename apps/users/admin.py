"""Application 'users' admin page configuration."""
from django.contrib import admin

from apps.recipes.models import User

admin.site.unregister(User)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Manage users."""

    list_filter = ('username', 'email',)
