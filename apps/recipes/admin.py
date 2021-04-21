"""Application 'recipes' admin page configuration."""
from django.contrib import admin
from django.db.models import Count

from apps.recipes.models import (
    Ingredient,
    Favorite,
    Follow,
    Purchase,
    Recipe,
    RecipeComposition,
    Tag,
    User)

admin.site.register((RecipeComposition, Favorite, Follow, Purchase))
admin.site.unregister(User)


class CompositionInline(admin.TabularInline):
    """Inline class for ingredients in recipes."""

    model = RecipeComposition
    extra = 0


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Manage users."""

    list_filter = ('username', 'email',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Manage recipes."""

    list_display = (
        'author',
        'title',
        'slug',
        'in_favorites_count',
    )

    search_fields = (
        'title',
    )
    list_filter = (
        'author',
        'title',
        'tags',
    )
    empty_value_display = '-пусто-'
    prepopulated_fields = {'slug': ('title',)}
    inlines = (CompositionInline,)

    def get_queryset(self, request):
        """Add annotated field."""
        queryset = super().get_queryset(request)
        return queryset.annotate(in_favorites=Count('favorite'))

    def in_favorites_count(self, recipe):
        """Get favorites count."""
        return recipe.in_favorites

    in_favorites_count.short_description = 'В избранном'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Manage tags."""

    list_display = (
        'pk',
        'title',
        'slug',
        'description',
        'style',
    )
    search_fields = (
        'title',
        'slug',
    )
    empty_value_display = '-пусто-'
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Manage ingredients."""

    list_display = (
        'pk',
        'name',
        'unit',
        'hasQuantity',
    )
    search_fields = (
        'name',
    )
    list_filter = (
        'name',
    )
    empty_value_display = '-пусто-'
