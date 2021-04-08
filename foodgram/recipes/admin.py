from django.contrib import admin

from recipes.models import Recipe, Tag, Ingredient


class TagsInline(admin.TabularInline):
    model = Tag.recipe.through
    extra = 0


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Manage recipes."""

    list_display = (
        'title',
        'text',
        'pub_date',
        'author',
        'image',
        'time',
        'slug',
    )
    search_fields = (
        'title',
    )
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'
    prepopulated_fields = {'slug': ('title',)}
    inlines = (TagsInline,)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Manage tags."""

    list_display = (
        'pk',
        'title',
        'slug',
        'description',
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
        'title',
        'unit',
        'hasQuantity',
    )
    search_fields = (
        'title',
    )
    empty_value_display = '-пусто-'
