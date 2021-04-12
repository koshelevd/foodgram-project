from django.forms import ModelForm

from recipes.models import Recipe


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ('text', 'group', 'image',)
        help_texts = {
            'text': 'Содержание вашей записи (обязательное поле)',
            'group': 'Укажите сообщество (необязательно)',
            'image': 'Загрузите изображение (необязательно)',
        }