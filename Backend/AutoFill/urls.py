from django.urls import path
from Backend.AutoFill.views import UserRegisterView, UserLoginView, VerifyEmail, ResendVerifyEmailCode
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('register', UserRegisterView.as_view()),
    path('login', UserLoginView.as_view()),
    path('veryfyemailaddress', VerifyEmail.as_view(), name="veryfyemailaddress"),
    path('resendveryfyemailcode', ResendVerifyEmailCode.as_view(), name="resendemailverification"),
    path('login/token/refresh/',TokenRefreshView.as_view(),name="token_refresh"),
    path('login/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]