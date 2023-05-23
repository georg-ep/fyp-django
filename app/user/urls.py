from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from user import views

app_name = 'user'

urlpatterns = [
    path('totp-secret/', views.GenerateTOTPUri.as_view(), name="generate-totp"),
    path('verify-totp-token/', views.VerifyTOTP.as_view(), name="verify-totp"),
    path('delete/', views.DeleteView.as_view(), name="delete"),
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('update/', views.UpdateView.as_view(), name='update'),
    path('auth/', views.TokenObtainPairView.as_view(), name='token_obtain'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('password/change/', views.ChangePasswordView.as_view(), name='password_change'),
    path('password/reset/confirm/', views.ConfirmResetPasswordView.as_view(), name="custom_password_reset"),
    path('password/reset/', include('django_rest_passwordreset.urls', namespace='password_generate')),
    path('detail/', views.DetailView.as_view(), name='detail'),
]
