from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.core import mail

from rest_framework import status
from rest_framework.test import APIClient
from django_rest_passwordreset.models import ResetPasswordToken

RESISTER_USER_URL = reverse('user:register')
AUTH_USER_URL = reverse('user:token_obtain')
REFRESH_TOKEN_URL = reverse('user:token_refresh')
VALIDATE_TOKEN_URL = reverse('user:password_reset:reset-password-validate')
PASSWORD_RESET_URL = reverse('user:password_reset:reset-password-request')
PASSWORD_RESET_CONFIRM_URL = reverse('user:password_reset:reset-password-confirm')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class UserApiTests(TestCase):
    """Test the users API. For coverage use: coverage run --omit=*/migrations/* manage.py test user"""

    def setUp(self):
        self.client = APIClient()

    # User registration tests
    def test_user_exists(self):
        """Test creating user that already exists fails"""
        payload = {
            'email': 'novak@pfld.cz',
            'password': '12345678',
        }
        create_user(**payload)
        response = self.client.post(RESISTER_USER_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)