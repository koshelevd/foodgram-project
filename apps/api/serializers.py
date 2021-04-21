"""Serializers of the 'api' app."""
from rest_framework import serializers
from rest_framework.fields import HiddenField, CurrentUserDefault

from apps.recipes.models import Favorite, Follow, Ingredient, Purchase


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


class PurchaseSerializer(CurrentUserDefault, serializers.ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        """Adds meta-information."""

        fields = '__all__'
        model = Purchase


class FollowSerializer(CurrentUserDefault, serializers.ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        """Adds meta-information."""

        fields = '__all__'
        model = Follow
