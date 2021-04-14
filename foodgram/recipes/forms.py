from django.forms import ModelForm, inlineformset_factory, Textarea, \
    CheckboxSelectMultiple

from recipes.models import Recipe, RecipeComposition


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ('title', 'description', 'tags','image', 'time', 'slug',
                  'ingredients',)
        help_texts = {
            # 'text': 'Содержание вашей записи (обязательное поле)',
            # 'group': 'Укажите сообщество (необязательно)',
            # 'image': 'Загрузите изображение (необязательно)',
        }
        widgets = {
            'description': Textarea(attrs={'rows': 8}),
            'tags': CheckboxSelectMultiple(),
        }

# class IngredientForm(ModelForm):
#     class Meta:
#         model = RecipeComposition
#
# IngredientFormset = inlineformset_factory(Recipe, RecipeComposition,
#                                           form=IngredientForm, extra=2)