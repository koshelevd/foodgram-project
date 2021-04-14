from django.core.exceptions import ValidationError
from django.forms import ModelForm, inlineformset_factory, Textarea, \
    CheckboxSelectMultiple, HiddenInput

from recipes.models import Recipe, RecipeComposition


class RecipeForm(ModelForm):
    def clean(self):
        # cleaned_data = super().clean()
        self.errors['ingredients'].pop()
        error_message =  ValidationError('Ingredients are empty!')
        self.add_error('ingredients', error_message)
        # return cleaned_data

    def get_ingredients(request):
        for key in request.POST:
            print(key)

    class Meta:
        model = Recipe
        fields = ('title', 'description', 'tags','image', 'time', 'slug',
                  'ingredients')
        help_texts = {
            # 'text': 'Содержание вашей записи (обязательное поле)',
            # 'group': 'Укажите сообщество (необязательно)',
            # 'image': 'Загрузите изображение (необязательно)',
        }
        widgets = {
            'description': Textarea(attrs={'rows': 8}),
            'tags': CheckboxSelectMultiple(),
        }


class IngredientForm(ModelForm):
    class Meta:
        model = RecipeComposition
        fields = ['ingredient', 'quantity',]
        widgets = {
            # 'ingredient': HiddenInput(),
        }

IngredientFormset = inlineformset_factory(Recipe, RecipeComposition,
                                          form=IngredientForm, extra=2)