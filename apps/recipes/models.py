"""Contains models to provide an Object-relational Mapping in 'foodgram'."""
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Recipe(models.Model):
    """
    Stores a single Recipe entry.
    """

    title = models.CharField(
        max_length=200,
        verbose_name='Название рецепта',
    )
    description = models.TextField(
        verbose_name='Содержание рецепта',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата публикации',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_index=True,
        related_name='recipes',
        verbose_name='Автор',
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        blank=True,
        through='RecipeComposition',
        related_name='recipes',
        verbose_name='Тэги',
    )
    tags = models.ManyToManyField(
        'Tag',
        db_index=True,
        related_name='recipes',
        verbose_name='Тэги',
    )
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name='Изображение',
    )
    time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
    )
    slug = models.SlugField(
        max_length=250,
        db_index=True,
        blank=True,
        unique=True,
        verbose_name='ЧПУ рецепта',
    )

    def __str__(self):
        """Return recipes's info."""
        return f'pk={self.pk} by {self.author}, {self.pub_date}'

    class Meta():
        ordering = ('-pub_date',)
        verbose_name_plural = 'Рецепты'
        verbose_name = 'Рецепт'


class Tag(models.Model):
    """Stores a single tag entry. """

    title = models.CharField(
        max_length=200,
        db_index=True,
        verbose_name='Название тэга',
    )
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
    style = models.CharField(
        max_length=50,
        default='orange',
        verbose_name='Css постфикс тэга',
    )

    def __str__(self):
        """Return overrided title of the tag."""
        return self.title

    class Meta():
        verbose_name_plural = 'Тэги'
        verbose_name = 'Тэг'


class Ingredient(models.Model):
    """Stores a single ingredient entry."""

    name = models.CharField(
        max_length=200,
        db_index=True,
        verbose_name='Название ингредиента',
    )
    unit = models.CharField(
        max_length=50,
        verbose_name='Единица измерения',
    )

    def __str__(self):
        """Return overrided title of the ingredient."""
        return f'{self.name}, {self.unit}'

    class Meta():
        verbose_name_plural = 'Ингредиенты'
        verbose_name = 'Ингредиент'


class RecipeComposition(models.Model):
    """
    Stores recipes and ingredients links.
    """

    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        db_index=True,
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
        unique_together = ('recipe', 'ingredient',)
        verbose_name_plural = 'Составы рецептов'
        verbose_name = 'Состав рецепта'


class Favorite(models.Model):
    """
    Stores recipes and ingredints links.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_index=True,
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
        unique_together = ('user', 'recipe',)
        verbose_name_plural = 'Избранное'
        verbose_name = 'Избранное'


class Follow(models.Model):
    """
    Stores followers and followings links.
    """

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_index=True,
        related_name='following',
        verbose_name='Автор',
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )

    def __str__(self):
        """Return followers's info."""
        return (f'Follow "{self.author}", '
                f'follower="{self.user}"')

    class Meta():
        """Adds meta-information."""

        unique_together = ('author', 'user',)
        verbose_name_plural = 'Подписчики'
        verbose_name = 'Подписчик'


class Purchase(models.Model):
    """
    Stores recipes and users links.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_index=True,
        related_name='purchase',
        verbose_name='Пользователь',
    )

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='purchase',
        verbose_name='Рецепт',
    )

    def __str__(self):
        """Return purchase info."""
        return f'Author "{self.user}", Recipe "{self.recipe}"'

    class Meta():
        unique_together = ('user', 'recipe',)
        verbose_name_plural = 'Список покупок'
        verbose_name = 'Покупка'
