"""Serializers of the 'api' app."""
from rest_framework import serializers

from recipes.models import Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        """Adds meta-information."""

        fields = '__all__'
        model = Ingredient
