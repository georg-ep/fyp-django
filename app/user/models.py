from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core import exception
from core.models import safe_file_path
from core.validators import validate_file_size
from django.core.validators import MinLengthValidator
from datetime import date


class UserManager(BaseUserManager):
    """User manager class for creating users and superusers"""

    def create_user(self, username: str, password: str = None, **extra_fields: dict) -> 'User':
        """
        Creates and saves new user
        :param username: user username
        :param password: user password
        :param extra_fields: additional parameters
        :return: created user model
        """
        if not username:
            raise exception.get(ValueError, 'User must have a username')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username: str, password: str) -> 'User':
        """
        Creates and saves new super user
        :param username: user username
        :param password: user password
        :return: created user model
        """
        user = self.create_user(username, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    username = models.CharField(
        max_length=255,
        unique=True,
        error_messages={'unique': "Username already used"},
        verbose_name = _("Username"),
        validators=[MinLengthValidator(8)],
    )
    dob = models.DateField(default=None, null=True, blank=True)
    gender = models.CharField(max_length=255, default=None, null=True, blank=True)
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_("Created at")
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    activities = models.ManyToManyField("logs.Activity", related_name="users")

    objects = UserManager()
    
    USERNAME_FIELD = 'username'
