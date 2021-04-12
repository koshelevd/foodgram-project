from django.contrib import admin

from recipes.models import Ingredient, Recipe, RecipeComposition, Tag


class CompositionInline(admin.TabularInline):
    model = RecipeComposition
    extra = 0


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Manage recipes."""

    list_display = (
        'pub_date',
        'author',
        'title',
        'slug',
    )
    fields = (
        'author',
        'title',
        'slug',
        'text',
        'time',
        'image',
        'tags',
    )
    search_fields = (
        'title',
    )
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'
    prepopulated_fields = {'slug': ('title',)}
    inlines = (CompositionInline,)


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
    empty_value_display = '-пусто-'
