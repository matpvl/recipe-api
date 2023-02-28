"""
Serializers for the user API view.
"""
from django.contrib.auth import get_user_model

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = get_user_model()
        # We only allow fields that the user would be able to change through the API
        # providing 'is_staff' and 'is_active' would be a security breach as it's reserved only for admin.
        fields = ["email", "password", "name"]
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        # This method will only be called after validation.
        return get_user_model().objects.create_user(**validated_data)
