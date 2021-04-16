from django.core.exceptions import ValidationError, BadRequest
from django.db import transaction, IntegrityError
from django.forms import ModelForm, inlineformset_factory, Textarea, \
    CheckboxSelectMultiple, HiddenInput
from django.http import HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import get_object_or_404
from pytils.translit import slugify

from recipes.models import Recipe, RecipeComposition, Ingredient


class RecipeForm(ModelForm):

    def __init__(self, *args, **kwargs):
        self.ingredients = {}
        super(RecipeForm, self).__init__(*args, **kwargs)

    def save(self, user, commit=False):
        try:
            with transaction.atomic():
                recipe = super().save(commit=commit)
                recipe.author = user
                recipe.slug = slugify(self.cleaned_data['title'])
                recipe.save()
                self.delete_compositions(recipe)
                self.update_or_create_compositions(recipe)
                self.save_m2m()
        except IntegrityError:
            raise BadRequest('Error while saving')
        return recipe

    def delete_compositions(self, recipe):
        existed_ingredients = recipe.composition.all()
        for row in existed_ingredients:
            if (row.ingredient.name,
                row.quantity) not in self.ingredients.items():
                row.delete()
            else:
                del self.ingredients[row.ingredient.name]



    def update_or_create_compositions(self, recipe):
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
        self.get_ingredients()
        cleaned_data = super().clean()
        if 'ingredients' in self.errors:
            del self.errors['ingredients']

        if not self.ingredients:
            error_message = ValidationError('Ingredients are empty!')
            self.add_error('ingredients', error_message)

        return cleaned_data

    def get_ingredients(self):
        for key, ingredient_name in self.data.items():
            if key.startswith('nameIngredient'):
                ingredient_value = self.data['valueIngredient' + key[14:]]
                self.ingredients[ingredient_name] = float(ingredient_value)

    class Meta:
        model = Recipe
        fields = ('title', 'description', 'tags', 'image', 'time', 'slug')
        widgets = {
            'description': Textarea(attrs={'rows': 8}),
            'tags': CheckboxSelectMultiple(),
        }
