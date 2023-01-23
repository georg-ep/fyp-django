from rest_framework import serializers
from rest_framework.serializers import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import ugettext_lazy as _


from logs import models as log_models
from logs import serializers as log_serializers
from user.models import User
from datetime import datetime
from django.db.models import F, Func, Sum


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for User model
    """

    password = serializers.CharField(write_only=True)
    username = serializers.CharField(write_only=True)
    gender = serializers.CharField(write_only=True)
    dob = serializers.DateField(write_only=True)

    access = serializers.SerializerMethodField()
    refresh = serializers.SerializerMethodField()

    def get_access(self, obj: User) -> str:
        """
        Returns user access token for authentication
        """
        refresh_token = RefreshToken.for_user(obj)
        return str(refresh_token.access_token)

    def get_refresh(self, obj: User) -> str:
        """
        Returns user refresh token for authentication
        """
        refresh_token = RefreshToken.for_user(obj)
        return str(refresh_token)

    def create(self, validated_data: dict) -> User:
        """
        Creates and saves user from validated data
        :param validated_data: dict of user parameters
        :return: created user
        """
        validated_data["username"] = validated_data["username"].lower()
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        try:
            user.save()
        except Exception:
            raise ValidationError(_("Already registered"))
        return user

    class Meta:
        model = User
        fields = (
            "username",
            "access",
            "refresh",
            "password",
            "dob",
            "gender",
        )


class UserDetailSerializer(serializers.ModelSerializer):
    activities = log_serializers.ActivitySerializer(many=True)

    class Meta:
        model = User
        fields = ("id", "username", "activities", "dob", "gender",)




class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "dob", "gender",)


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(
        write_only=True, allow_null=False, allow_blank=False
    )
    new_password = serializers.CharField(
        write_only=True, allow_blank=False, allow_null=False
    )

    def create(self, validated_data: dict) -> User:
        old_password = validated_data.get("old_password")
        new_password = validated_data.get("new_password")

        user = self.context.get("request").user

        if not user.check_password(old_password):
            raise ValidationError("Invalid old password")

        user.set_password(new_password)
        user.save()
        return user

    class Meta:
        model = User
        fields = ("old_password", "new_password")

