"""Serializers of the 'api' app."""
from rest_framework import serializers

from apps.api.models import Favorite
from apps.recipes.models import Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        """Adds meta-information."""

        fields = '__all__'
        model = Ingredient


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        """Adds meta-information."""

        fields = '__all__'
        model = Favorite
