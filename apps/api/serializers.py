"""Serializers of the 'api' app."""
from rest_framework import serializers
from rest_framework.fields import HiddenField, CurrentUserDefault

from apps.api.models import Favorite
from apps.recipes.models import Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        """Adds meta-information."""

        fields = '__all__'
        model = Ingredient


class FavoriteSerializer(CurrentUserDefault, serializers.ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        """Adds meta-information."""

        fields = '__all__'
        model = Favorite
