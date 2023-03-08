"""
Serializers for recipe APIs.
"""
from rest_framework import serializers

from core.models import Recipe, Tag


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags."""

    class Meta:
        model = Tag
        fields = ["id", "name"]
        read_only_fields = ["id"]


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipes."""
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = ["id", "title", "time_minutes", "price", "link", "tags"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        """Create a recipe."""
        # If tags exist in validated data, we will remove it, and
        # add it to a new variable called tags, if it does not exist
        # we will just use it as an empty list.
        tags = validated_data.pop('tags', [])
        # Django expects tags to be created separately, so we create custom logic.
        recipe = Recipe.objects.create(**validated_data)
        auth_user = self.context['request'].user
        for tag in tags:
            # get_or_create is a Model Manager helper function which will get the
            # value if it exists for the user and Tag.name that's provided, or create one.
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                **tag
            )
            recipe.tags.add(tag_obj)

        return recipe


# We are using RecipeSerializer as the base class of RecipeDetailSerializer,
# since RecipeDetailSerializer will serve as an extension of the RecipeSerializer.
class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detail view."""

    # We also have to specify the Meta class inheritance in this case.
    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ["description"]
