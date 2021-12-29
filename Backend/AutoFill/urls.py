from django.urls import path
from Backend.AutoFill.views import UserRegisterView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('register', UserRegisterView.as_view()),
    path('login/token/refresh/',TokenRefreshView.as_view(),name="token_refresh"),
    path('login/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]