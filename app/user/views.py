from django_rest_passwordreset.serializers import PasswordTokenSerializer
from django.utils.translation import ugettext_lazy as _
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from django_rest_passwordreset.views import ResetPasswordConfirm
from user.models import User

from user import serializers


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

