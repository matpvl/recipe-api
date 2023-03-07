"""
Serializers for recipe APIs.
"""
from rest_framework import serializers

from core.models import Recipe, Tag


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipes."""

    class Meta:
        model = Recipe
        fields = ["id", "title", "time_minutes", "price", "link"]
        read_only_fields = ["id"]


# We are using RecipeSerializer as the base class of RecipeDetailSerializer,
# since RecipeDetailSerializer will serve as an extension of the RecipeSerializer.
class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detail view."""

    # We also have to specify the Meta class inheritance in this case.
    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ["description"]


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags."""

    class Meta:
        model = Tag
        fields = ["id", "name"]
        read_only_fields = ["id"]
