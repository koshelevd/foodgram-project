"""Application 'recipes' forms."""
from uuid import uuid4

from django.core.exceptions import BadRequest, ValidationError
from django.db import IntegrityError, transaction
from django.forms import (CheckboxSelectMultiple,
                          ModelForm,
                          SelectMultiple,
                          Textarea)
from django.shortcuts import get_object_or_404
from pytils.translit import slugify

from apps.recipes.models import Ingredient, Recipe, RecipeComposition


class TagForm(ModelForm):
    """Model form for recipes filter."""

    class Meta:
        model = Recipe
        fields = ('tags',)
        widgets = {
            'tags': SelectMultiple(),
        }


class RecipeForm(ModelForm):
    """Model form for create, update and delete form."""

    def __init__(self, *args, **kwargs):
        """Init ingredients variable to store ingredients data from form."""
        self.ingredients = {}
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        """Save recipe's data."""
        user = kwargs.get('user')
        try:
            with transaction.atomic():
                recipe = super().save(commit=False)
                if recipe.author_id is None:
                    recipe.author = user
                slug = slugify(self.cleaned_data['title'])
                if Recipe.objects.filter(slug=slug).exists():
                    slug = uuid4()
                recipe.slug = slug
                recipe.save()
                self.delete_compositions(recipe)
                self.create_compositions(recipe)
                self.save_m2m()
        except IntegrityError as save_error:
            raise BadRequest('Error while saving') from save_error
        return recipe

    def delete_compositions(self, recipe):
        """Delete compositions in case of recipe's edit."""
        existed_ingredients = recipe.compositions.all()
        for row in existed_ingredients:
            if (row.ingredient.name,
                row.quantity) not in self.ingredients.items():
                row.delete()
            else:
                del self.ingredients[row.ingredient.name]

    def create_compositions(self, recipe):
        """Create compositions for ingredients."""
        compositions_to_create = []
        for ingredient_name, quantity in self.ingredients.items():
            ingredient = get_object_or_404(Ingredient,
                                           name=ingredient_name)
            composition = RecipeComposition(recipe=recipe,
                                            ingredient=ingredient,
                                            quantity=quantity)
            compositions_to_create.append(composition)
        RecipeComposition.objects.bulk_create(compositions_to_create)

    def clean(self):
        """Validate ingredients data."""
        self.get_ingredients()
        cleaned_data = super().clean()
        if not self.ingredients:
            error_message = ValidationError('Ingredients are empty!')
            self.add_error(None, error_message)
        return cleaned_data

    def get_ingredients(self):
        """Extract ingredients from POST data."""
        for key, ingredient_name in self.data.items():
            if key.startswith('nameIngredient'):
                ingredient_value = self.data['valueIngredient' + key[14:]]
                self.ingredients[ingredient_name] = float(ingredient_value)

    class Meta:
        model = Recipe
        fields = ('title', 'description', 'tags', 'image', 'time', 'slug',)
        widgets = {
            'description': Textarea(attrs={'rows': 8}),
            'tags': CheckboxSelectMultiple(),
        }
