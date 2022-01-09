from django.urls import path
from Backend.AutoFill.views import UserRegisterView, UserLoginView, VerifyEmail, ResendVerifyEmailCode, BasicInfoRegisteration, SendMailSetting, \
    AddStopLinks, DmClickedCountCalculation, Maildeliverystoptext, MesurmentMethodSet, Getmesurmentmethodsetting
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('register', UserRegisterView.as_view()),
    path('login', UserLoginView.as_view()),
    path('veryfyemailaddress', VerifyEmail.as_view(), name="veryfyemailaddress"),
    path('resendveryfyemailcode', ResendVerifyEmailCode.as_view(), name="resendemailverification"),
    path('basicInfoRegister', BasicInfoRegisteration.as_view()),    
    path('sendMailSetting', SendMailSetting.as_view()),   
    path('addstoplinks', AddStopLinks.as_view()),
    path('dmclicked', DmClickedCountCalculation.as_view()),
    path('maildeliverystoptext', Maildeliverystoptext.as_view()),
    path('mesurmentmethodsetting', MesurmentMethodSet.as_view()),
    path('getmesurmentmethodsetting', Getmesurmentmethodsetting.as_view()),
    path('login/token/refresh/',TokenRefreshView.as_view(),name="token_refresh"),
    path('login/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
]