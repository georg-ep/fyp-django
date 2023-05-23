from rest_framework import serializers
from rest_framework.serializers import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import ugettext_lazy as _
from core.encryption import encrypt, decrypt

from logs import models as log_models
from user.models import User
from .utils import generate_totp_secret

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import re

class TokenObtainSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        attrs['email'] = encrypt(attrs['email'])
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['lifetime'] = int(refresh.access_token.lifetime.total_seconds())
        return data

class DeleteUserSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True)

    def delete(self, validated_data):
        user = self.context.get("request").user
        password = validated_data.get("password")
        
        if not user.check_password(password):
            raise ValidationError("This password is incorrect")
        
        # return super().destory(validated_data)
        return False
          

class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for User model
    """

    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    email = serializers.CharField(write_only=True)
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
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        validated_data["email"] = validated_data["email"].lower()

        if not re.fullmatch(regex, validated_data["email"]):
            raise ValidationError("Invalid email format")
        
        password_regex = re.compile(r'(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_\-+=|{}[\]:;<>?,./]).{12,}$')
        if not re.fullmatch(password_regex, validated_data.get("password")):
            raise ValidationError("Password must be 12+ characters and include one uppercase, lowercase, number and symbol")

        if not validated_data["confirm_password"] == validated_data["password"]:
            raise ValidationError("Passwords don't match")
        
        del validated_data["confirm_password"]
        
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.totp_secret = generate_totp_secret()

        user.email = encrypt(user.email)
        user.dob = encrypt(str(user.dob))

        try:
            user.save()
        except Exception:
            raise ValidationError(_("Already registered"))
        return user

    class Meta:
        model = User
        fields = (
            "email",
            "access",
            "refresh",
            "password",
            "dob",
            "totp_enabled",
            "confirm_password"
        )


class UserDetailSerializer(serializers.ModelSerializer):
    total_cycles = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    dob = serializers.SerializerMethodField()

    def get_total_cycles(self, obj):
        user = self.context["request"].user
        return log_models.BreathingCycle.objects.filter(mood_before__user=user).count()

    class Meta:
        model = User
        fields = ("id", "email", "dob", "total_cycles", "totp_enabled",)
    
    def get_email(self, obj):
        return self.context["request"].user.get_email
    
    def get_dob(self, obj):
        return self.context["request"].user.get_dob



class UserUpdateSerializer(serializers.ModelSerializer):
    
    def update(self, instance, validated_data):
        user = instance

        if not validated_data.get("email"):
            raise ValidationError("There was an issue with the details you entered")

        if User.objects.filter(email=encrypt(user.email)).exists():
            raise ValidationError("This email already exists")
        
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if not re.fullmatch(regex, validated_data["email"]):
            raise ValidationError("Invalid email format")
        

        user.email = encrypt(validated_data.get("email"))
        user.dob = encrypt(validated_data.get("dob"))

        user.save()

        return user

        

    class Meta:
        model = User
        fields = ("email", "dob", "totp_enabled",)


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

