from rest_framework import permissions
# from Akushu.settings import DATABASES, MEDIA_ROOT
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
# from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from Backend.AutoFill.serializers import UserLoginSerializer, UserRegistrationSerializer
from Backend.AutoFill.models import User
from django.db.models import Q
# from django.db import connection
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404, render
# from rest_framework_jwt.settings import api_settings
import uuid
from django.core import serializers

from rest_framework.parsers import MultiPartParser, FormParser
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import stripe
from django.core.mail import send_mail
from random import randint


class UserRegisterView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)
    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data = data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = get_object_or_404(User, email=data['email'])
        verificationCode = random_with_N_digits(6)
        user.verificationcode = verificationCode
        user.save()
        print(verificationCode)
        # subject = 'Akushu APPに正常に登録しました。'
        # message = '検証コード' + str(verificationCode)

        # send_mail_to(user.email,subject, message)
        status_code = status.HTTP_201_CREATED
        response = {
            'success': 'True',
            'status code': status_code,
            'type': 'User registered  successfully',
        }
        return Response(response, status=status_code)
        


def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def send_mail_to(useremail, subject, message):
    email_from = settings.SERVER_EMAIL
    recipient_list = [useremail]
    send_mail(subject, message, email_from, recipient_list)
    return True