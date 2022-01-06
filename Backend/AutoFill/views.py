from rest_framework import permissions
# from Akushu.settings import DATABASES, MEDIA_ROOT
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
# from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from Backend.AutoFill.serializers import UserLoginSerializer, UserRegistrationSerializer
from Backend.AutoFill.models import User, SendMailSettingModel
from django.db.models import Q
# from django.db import connection
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404, render
# from rest_framework_jwt.settings import api_settings
import uuid
from django.core import serializers
import os
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
        # subject = '正常に登録しました。'
        # message = '検証コード' + str(verificationCode)

        # send_mail_to(user.email,subject, message)
        status_code = status.HTTP_201_CREATED
        response = {
            'success': 'true',
            'status code': status_code, 
            'email':user.email,
            'type': 'User registered  successfully',
        }
        return Response(response, status=status_code)
        
class UserLoginView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data= request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            'status code' : status.HTTP_200_OK,
            'statusText': 'OK',
            'token' : serializer.data['token'],
            'refresh':serializer.data['refresh'],
            'userstatus':serializer.data['userstatus'],
            'email':serializer.data['email']
        }
        status_code = status.HTTP_200_OK
        return Response(response, status=status_code)


class VerifyEmail(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        data = request.data
        user = get_object_or_404(User, email=data['mail'])
        if user == None:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                'success': 'False',
                'status code': status_code,
            }
        else:
            if (user.verificationcode == data['vc']):
                user.userstatus = 1
                user.verificationcode = ''
                user.save()
                status_code = status.HTTP_200_OK
                response = {
                    'success': 'True',
                    'status code': status_code,
                }
            else:
                status_code = status.HTTP_400_BAD_REQUEST
                response = {
                    'success': 'False',
                    'status code': status_code
                }
        return Response(response, status=status_code)


class ResendVerifyEmailCode(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        user = request.user
        verificationCode = random_with_N_digits(6)
        user.verificationcode = verificationCode
        user.save()
        subject = 'Akushu APPに正常に登録しました。'
        message = '検証コード' + str(verificationCode)

        send_mail_to(user.email,subject, message)
        status_code = status.HTTP_200_OK
        response = {
            'success': 'True',
            'status code': status_code
        }
        return Response(response, status=status_code)


class BasicInfoRegisteration(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        basicdata = request.data 
        user = request.user
        user.coporate_name = basicdata['coporate_name']
        user.company_type = basicdata['company_type']
        user.corporate_furigana = basicdata['corporate_furigana']
        user.corporate_zipcode = basicdata['corporate_zipcode']
        user.corporate_country = basicdata['corporate_country']
        user.corporate_prefecture = basicdata['corporate_prefecture']
        user.corporate_city = basicdata['corporate_city']
        user.corporate_address = basicdata['corporate_address']
        user.corporate_building_name = basicdata['corporate_building_name']
        user.corporate_estable_date = basicdata['corporate_estable_date']
        user.corporate_phone = basicdata['corporate_phone']
        user.corporate_fax = basicdata['corporate_fax']
        user.corporate_mail = basicdata['corporate_mail']
        user.corporate_homepage = basicdata['corporate_homepage']
        user.corporate_address_room_number = basicdata['corporate_address_room_number']
        user.firstname_of_charger = basicdata['firstname_of_charger']
        user.lastname_of_charger = basicdata['lastname_of_charger']
        user.firstname_of_charger_firagana = basicdata['firstname_of_charger_firagana']
        user.lastname_of_charger_firagana = basicdata['lastname_of_charger_firagana']
        user.charger_prefecture = basicdata['charger_prefecture']
        user.choice_word = basicdata['choice_word'] 
        oldavatar = user.avatar
        avatarimgFile =  request.FILES.get('avatar', '')
        fs = FileSystemStorage()
        if(avatarimgFile):
            if oldavatar:
                oldavatarPath = os.path.join(settings.MEDIA_ROOT, oldavatar)
                if os.path.isfile(oldavatarPath):
                    os.remove(oldavatarPath)
            filename = fs.save(avatarimgFile.name, avatarimgFile)
            user.avatar = filename  
        
        user.save()
        status_code = status.HTTP_200_OK
        response = {
            'success':'True',
            'status code': status_code,
            'type':'Profile Update'
        }
        return Response(response, status=status_code)


class SendMailSetting(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):        
        user = request.user
        data = request.data 
        SendMailSettingModel.objects.create(
            name = data['name'],
            sendmail = data['sendmail'],
            replytodmail = data['replytodmail'],
            smtp = data['smtp'],
            mailid = data['mailid'],
            mailpwd =  data['mailpwd'],
            mailport =  data['mailport'],
            mailssl =  data['mailssl'],
            popcheck = data['popcheck'],
            popserver = data['popserver'],
            username = data['username'],
            userpwd = data['userpwd'], 
            user = user,            
        )

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