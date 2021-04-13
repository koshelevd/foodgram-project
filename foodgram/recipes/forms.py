from django.forms import ModelForm, inlineformset_factory

from recipes.models import Recipe, RecipeComposition


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ('title', 'description', 'image', 'time', 'slug',
                  'ingredients',)
        help_texts = {
            # 'text': 'Содержание вашей записи (обязательное поле)',
            # 'group': 'Укажите сообщество (необязательно)',
            # 'image': 'Загрузите изображение (необязательно)',
        }

# class IngredientForm(ModelForm):
#     class Meta:
#         model = RecipeComposition
#
# IngredientFormset = inlineformset_factory(Recipe, RecipeComposition,
#                                           form=IngredientForm, extra=2)