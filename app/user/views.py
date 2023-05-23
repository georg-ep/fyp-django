from django_rest_passwordreset.serializers import PasswordTokenSerializer
from django.utils.translation import ugettext_lazy as _
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from django_rest_passwordreset.views import ResetPasswordConfirm
from user.models import User

from user import serializers
from .utils import generate_totp_uri, verify_totp_token
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json

from rest_framework_simplejwt.views import TokenViewBase


class TokenObtainPairView(TokenViewBase):
    serializer_class = serializers.TokenObtainSerializer



class GenerateTOTPUri(APIView):
    permissions_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        uri = generate_totp_uri(request.user.totp_secret, request.user.email, 'WBA')
        return Response({'uri': uri})

class VerifyTOTP(APIView):
    permissions_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        secret = request.user.totp_secret
        token = request.data.get('token')
        if verify_totp_token(secret, token):
            return Response({'status': 'ok'}, status=status.HTTP_200_OK)
        return Response({'status': 'fail'}, status=status.HTTP_401_UNAUTHORIZED)
  
class DeleteView(APIView):
    queryset = User.objects.all()
    serializer_class = serializers.DeleteUserSerializer

    def post(self, request, *args, **kwargs):
        # return super().delete(request, *args, **kwargs)
        user = request.user
        body = json.loads(request.body.decode("utf-8"))
        password = body.get("password", "")
        
        if not password:
            return Response({"data": "Password is required"})

        if not user.check_password(password):
            return Response({"data":"This password is incorrect"}, status=status.HTTP_401_UNAUTHORIZED)
        
        user.delete()
        
        return Response({})


class RegistrationView(CreateAPIView):
    serializer_class = serializers.UserRegisterSerializer

class UpdateView(UpdateAPIView):
    serializer_class = serializers.UserUpdateSerializer
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user

class ChangePasswordView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ChangePasswordSerializer


class ConfirmResetPasswordView(ResetPasswordConfirm):
    serializer_class = PasswordTokenSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        status_message = response.data.get("status", None)

        if status_message is None:
            return response

        if status_message == "OK":
            return response

        message_map = {
            "notfound": _("Code is not found."),
            "expired": _("Code has expired.")
        }
        response.data["status"] = message_map[status_message]

        return response


class DetailView(RetrieveAPIView):
    serializer_class = serializers.UserDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

