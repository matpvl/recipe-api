"""
Serializers for the user API view.
"""
import datetime
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = get_user_model()
        # We only allow fields that the user would be able to change through the API
        # providing 'is_staff' and 'is_active' would be a security breach as it's reserved only for admin.
        fields = ["email", "password", "name", "birthday"]
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        # This method will only be called after validation.
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update and return user"""
        password = validated_data.pop("password", None)
        # We pop the password, so it isn't saved as plain text, and then update the name and email.
        user = super().update(instance, validated_data)

        # If the user has provided a password, then we use the .set_password() function to
        # encrypt it and save it.
        if password:
            user.set_password(password)
            user.save()

        date = validated_data.pop("birthday", None)
        # We allow the user to provide a null field, but if a date is provided it must be correct.
        if date is not None:
            # We check that the date is correct format.
            # UPDATE: Django provides date formating on its own, no need for this validation.
            # if not datetime.date.fromisoformat(str(date)):
            #     msg = _("Please input correct date format: YYYY-MM-DD.")
            #     raise serializers.ValidationError(msg, code="date_format")
            # We check that a future date isn't provided.
            if not date <= datetime.date.today():
                msg = _("Date of birth cannot be in the future.")
                raise serializers.ValidationError(msg, code="future_date")

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""

    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""
        email = attrs.get("email")
        password = attrs.get("password")
        user = authenticate(
            request=self.context.get("request"), username=email, password=password
        )
        if not user:
            msg = _("Unable to authenticate with provided credentials.")
            raise serializers.ValidationError(msg, code="authorization")
        return {"user": user}
