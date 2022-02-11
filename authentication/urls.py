from django.urls import path

from .views import (LoginView, PasswordTokenCheckAPI, RegisterView,
                    RequestPasswordResetEmail, SetPasswordAPIView,
                    VerifyEmailView)

app_name='authentication'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register-list'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('login/', LoginView.as_view(), name='login'),
    path('password-reset/<uidb64>/<token>/', PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('request-reset-email/', RequestPasswordResetEmail.as_view(), name='request-reset-email'),
    path('password-reset-complete/', SetPasswordAPIView.as_view(), name='password-reset-complete'),
]
