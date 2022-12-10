from unicodedata import name
from django.conf.urls import url
from authentication.views import UserAvatarUpload,EmailChecker,UnameChecker,ChangePwdAPIView, PasswordTokenCheckAPI, RegistrationView,PasswordResetEmail,UpdateProfileView,UnameSuggest
from authentication.views import VerifyEmail
from django.urls import path
from rest_framework_jwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from authentication.views import LoginAPIView
urlpatterns = [
    path('register/',RegistrationView.as_view(),name="register"),
    path('login/',LoginAPIView.as_view(),name="login"),
    path('update/',UpdateProfileView.as_view(),name="update"),
    path('email-verify/',VerifyEmail.as_view(),name="email-verify"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('request-reset-password',PasswordResetEmail.as_view(),name="request-reset-password"),
    path('password-reset/<uidb64>/<token>/',PasswordTokenCheckAPI.as_view(),name='password-reset-confirm'),
    path('password-reset-complete',ChangePwdAPIView.as_view(),name='password-reset-complete'),
    path('email-checker/',EmailChecker.as_view(),name="email-chekcer"),
    path('uname-checker/',UnameChecker.as_view(),name="uname-chekcer"),
    path('uname-suggest/',UnameSuggest.as_view(),name="uname-chekcer"),
    path('avatar-upload/',UserAvatarUpload.as_view(),name="avatar-upload"),

]
