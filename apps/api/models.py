from django.db import models

from apps.recipes.models import User, Recipe


class Favorite(models.Model):
    """
    Stores recipes and ingredints links.

    Related to :model:'recipes.Recipe', 'recipes.Ingredient'
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Пользователь',
    )

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Рецепт',
    )


    def __str__(self):
        """Return recipe composition info."""
        return f'Author "{self.user}", Recipe "{self.recipe}"'

    class Meta():
        """Adds meta-information."""

        unique_together = ('user', 'recipe',)
        verbose_name_plural = 'Избранное'
        verbose_name = 'Избранное'

