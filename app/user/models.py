from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core import exception
from django.core.validators import MinLengthValidator
from core.encryption import encrypt, decrypt

class UserManager(BaseUserManager):
    """User manager class for creating users and superusers"""

    def create_user(self, email: str, password: str = None, **extra_fields: dict) -> 'User':
        """
        Creates and saves new user
        :param username: user username
        :param password: user password
        :param extra_fields: additional parameters
        :return: created user model
        """
        if not email:
            raise exception.get(ValueError, 'User must have an email')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email: str, password: str) -> 'User':
        """
        Creates and saves new super user
        :param username: user username
        :param password: user password
        :return: created user model
        """
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.CharField(max_length=300, null=True, blank=True, default=None, unique=True)
    dob = models.CharField(max_length=255, default=None, null=True)
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_("Created at")
    )
    totp_secret = models.CharField(max_length=255, default=None, null=True, blank=True)
    totp_enabled = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    
    @property
    def get_email(self):
        return decrypt(self.email)
    
    @property
    def get_dob(self):
        return decrypt(self.dob)
