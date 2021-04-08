from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Recipe(models.Model):
    """
    Stores a single Recipe entry.

    Related to :model:'auth.User' and :model:'recipes.Tag'. !!!
    """

    title = models.CharField(
        max_length=200,
        verbose_name='Название рецепта',
    )
    text = models.TextField(
        verbose_name='Содержание рецепта',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
    )
    tags = models.ManyToManyField(
        'Tag',
        related_name='recipes',
        verbose_name='Тэги',
    )
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name='Изображение',
    )
    time = models.IntegerField(
        verbose_name='Время приготовления (мин.)',
    )
    slug = models.SlugField(
        max_length=250,
        unique=True,
        verbose_name='ЧПУ рецепта',
    )

    def __str__(self):
        """Return recipes's info."""
        return f'pk={self.pk} by {self.author}, {self.pub_date}'

    class Meta():
        """Adds meta-information."""

        ordering = ('-pub_date',)
        verbose_name_plural = 'Рецепты'
        verbose_name = 'Рецепт'


class Tag(models.Model):
    """Stores a single tag entry. """

    title = models.CharField(
        max_length=200,
        verbose_name='Название тэга',
    )
    # recipe = models.ManyToManyField(
    #     'Recipe',
    #     blank=True,
    #     related_name='tags',
    #     verbose_name='Рецепты',
    # )
    slug = models.SlugField(
        max_length=250,
        blank=True,
        null=True,
        unique=True,
        verbose_name='ЧПУ тэга',
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание тэга',
    )

    def __str__(self):
        """Return overrided title of the tag."""
        return self.title

    class Meta():
        """Adds meta-information."""

        verbose_name_plural = 'Тэги'
        verbose_name = 'Тэг'


class Ingredient(models.Model):
    """Stores a single ingredient entry."""

    title = models.CharField(
        max_length=200,
        verbose_name='Название ингредиента',
    )
    unit = models.CharField(
        max_length=10,
        verbose_name='Единица измерения',
    )
    hasQuantity = models.BooleanField(
        default=True,
        null=True,
        verbose_name='Содержит количество',
    )

    def __str__(self):
        """Return overrided title of the ingredient."""
        return f'{self.title}, {self.unit}'

    class Meta():
        """Adds meta-information."""

        verbose_name_plural = 'Ингредиенты'
        verbose_name = 'Ингредиент'


class RecipeComposition(models.Model):
    """
    Stores recipes and ingredints links.

    Related to :model:'recipes.Recipe', 'recipes.Ingredient'
    """

    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        related_name='composition',
        verbose_name='Рецепт',
    )

    ingredient = models.ForeignKey(
        'Ingredient',
        on_delete=models.CASCADE,
        related_name='composition',
        verbose_name='Ингредиент',
    )

    quantity = models.FloatField(
        blank=True,
        null=True,
        verbose_name='Количество',
    )

    def __str__(self):
        """Return recipe composition info."""
        return (f'Recipe "{self.recipe}", quantity="{self.quantity}"'
                f'ingredient="{self.ingredient}"')

    class Meta():
        """Adds meta-information."""

        unique_together = ('recipe', 'ingredient',)
        verbose_name_plural = 'Составы рецептов'
        verbose_name = 'Состав рецепта'
