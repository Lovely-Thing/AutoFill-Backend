from rest_framework import permissions
# from Akushu.settings import DATABASES, MEDIA_ROOT
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
# from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from Backend.AutoFill.serializers import UserLoginSerializer, UserRegistrationSerializer
from Backend.AutoFill.models import User, SendMailSettingModel, StopLinkSettingModel, DmClickedCountModel, MailDeliveryStopTextsModel, \
    MesurmentMethodSettingModel
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
from smtplib import SMTP_SSL, SMTP_SSL_PORT


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
        subject = '正常に登録しました。'
        message = '検証コード' + str(verificationCode)

        send_mail_to(data['email'] , subject, message)
        status_code = status.HTTP_201_CREATED
        response = {
            'success': 'true',
            'status code': status_code, 
            'email': data['email'],
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

class AddStopLinks(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):        
        user = request.user
        data = request.data 

        for d in data: 
            StopLinkSettingModel.objects.create(
                name = d['corporate_name'],
                mailaddress = d['mailaddress'],
                contact_url = d['contact_url'],
                site_url = d['site_url'],
                phone_num = d['phone'],
                auto_manual =  "手動", 
                user = user,            
            )

        status_code = status.HTTP_201_CREATED
        response = {
            'success': 'True',
            'status code': status_code,
            'type': 'User registered  successfully',
        }
        return Response(response, status=status_code)

class DmClickedCountCalculation(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):   
        data = request.data
        if data['mail_id'] !=None:
            dmcountdata = DmClickedCountModel.objects.filter(Q(mailid=data['mail_id'])).first()
            if dmcountdata :
                dmcountdata.clickednum = dmcountdata.clickednum + 1
                dmcountdata.save()
            else:
                DmClickedCountModel.objects.create(
                    clickednum = 1,
                    mailid = data['mail_id']          
                )

            status_code = status.HTTP_201_CREATED
            response = {
                'success': 'True',
                'status code': status_code,
                'type': 'User registered  successfully',
            }
            return Response(response, status=status_code)


class Maildeliverystoptext(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request): 
        user = request.user
        data = request.data 

        mailstoptext = MailDeliveryStopTextsModel.objects.filter(Q(user=user)).first()
        if mailstoptext :
            mailstoptext.text2000 = data['text2000']
            mailstoptext.text1000 = data['text1000']
            mailstoptext.text500 = data['text500']
            mailstoptext.text250 = data['text250']
            mailstoptext.text100 = data['text100']
            mailstoptext.save()
        else:
            MailDeliveryStopTextsModel.objects.create(
                text2000 = data['text2000'],
                text1000 = data['text1000'],
                text500 = data['text500'],
                text250 = data['text250'],
                text100 = data['text100'],
                user = user       
            )

        status_code = status.HTTP_201_CREATED
        response = {
            'success': 'True',
            'status code': status_code,
            'type': 'User registered  successfully',
        }
        return Response(response, status=status_code)

class MesurmentMethodSet(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request): 
        user = request.user
        data = request.data 

        method = MesurmentMethodSettingModel.objects.filter(Q(user=user)).first()
        if method :
            method.mesurment_method = data['mesurment_method'] 
            method.save()
        else:
            MesurmentMethodSettingModel.objects.create(
                mesurment_method = data['mesurment_method'], 
                user = user       
            )

        status_code = status.HTTP_201_CREATED
        response = {
            'success': 'True',
            'status code': status_code,
            'type': 'User registered  successfully',
        }
        return Response(response, status=status_code)


class Getmesurmentmethodsetting(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request): 
        user = request.user 

        method = MesurmentMethodSettingModel.objects.filter(Q(user=user)).first()
        print(method)
        if method :
            status_code = status.HTTP_200_OK
            response = {
                'success': 'True',
                'method':method.mesurment_method,
                'status code': status_code,
                'type': 'User registered  successfully',
            }
            return Response(response, status=status_code)

        else: 
            status_code = status.HTTP_200_OK
            response = {
                'success': 'True',
                'method': 1,
                'status code': status_code,
                'type': 'User registered  successfully',
            }
            return Response(response, status=status_code)

class TestSendMail(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        SMTP_HOST = 'mail.example.com'
        SMTP_USER = 'someone@example.com'
        SMTP_PASS = 'Secret!'

        # Craft the email by hand
        from_email = 'My name <someone@example.com>'  # or simply the email address
        to_emails = ['nanodano@devdungeon.com', 'admin@devdungeon.com']
        body = "Hello, world!"
        headers = f"From: {from_email}\r\n"
        headers += f"To: {', '.join(to_emails)}\r\n" 
        headers += f"Subject: Hello\r\n"
        email_message = headers + "\r\n" + body  # Blank line needed between headers and body

        # Connect, authenticate, and send mail
        smtp_server = SMTP_SSL(SMTP_HOST, port=SMTP_SSL_PORT)
        smtp_server.set_debuglevel(1)  # Show SMTP server interactions
        smtp_server.login(SMTP_USER, SMTP_PASS)
        smtp_server.sendmail(from_email, to_emails, email_message)

        # Disconnect
        smtp_server.quit()





    # def send_mail(subject='', text='', sender='', to=''):
    #     M = poplib.POP3(settings.EMAIL_HOST)
    #     M.user(settings.EMAIL_HOST_USER)
    #     M.pass_(settings.EMAIL_HOST_PASSWORD)
    #     headers = "From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n" % (sender,
    #     to, subject)
    #     message = headers + text
    #     mailServer = smtplib.SMTP(settings.EMAIL_HOST)
    #     mailServer.sendmail(sender, to, message)
    #     mailServer.quit()













        status_code = status.HTTP_200_OK
        response = {
            'success': 'True',
            'method': 1,
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