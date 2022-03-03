from gettext import find
from inspect import isframe
from turtle import st 
from anticaptchaofficial.recaptchav3proxyless import *
from anticaptchaofficial.hcaptchaproxyless import *
from anticaptchaofficial.recaptchav2proxyless import *
from cgi import print_directory
import email
from optparse import Option
from pickle import FALSE, NONE
from select import select
from sys import flags
from traceback import print_tb 
# from types import NoneType
from rest_framework import permissions
# from Akushu.settings import DATABASES, MEDIA_ROOT
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
# from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from Backend.AutoFill.serializers import UserLoginSerializer, UserRegistrationSerializer, AdminLoginSerializer
from Backend.AutoFill.models import User, SendMailSettingModel, StopLinkSettingModel, DmClickedCountModel, MailDeliveryStopTextsModel, \
    MesurmentMethodSettingModel, DMtextSetModel, DMGroupModel, PerDMGroupDmListModel, DMSendStatusModel
from django.db.models import Q
# from django.db import connection
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404, render
# from rest_framework_jwt.settings import api_settings
import uuid
from django.core import serializers
import os
from rest_framework.parsers import MultiPartParser, FormParser
from django.conf import UserSettingsHolder, settings
from django.core.files.storage import FileSystemStorage
import stripe
from django.core.mail import send_mail
from random import randint
from smtplib import SMTP_SSL, SMTP_SSL_PORT
from django.core.mail import send_mail
import datetime 
import pandas as pd
import json
import requests
from bs4 import BeautifulSoup 
from mechanize import Browser 
import time
import random
from datetime import date, datetime, time, timedelta
import threading as th  
from django.contrib.sessions.backends.db import SessionStore 
from django.db.models import Sum
import numpy as np  
import traceback 


ANTI_CAPTCHA_API_KEY = "360de08d894d78cfd722eedaa4e11204"
NoneType = type(None)
driver_lists = []

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
        subject = '正常に登録しました。'
        message = '検証コード' + str(verificationCode)

        send_mail_to(data['email'] , subject, message)
        status_code = status.HTTP_201_CREATED
        response = {
            'success': 'true',
            'status code': status_code, 
            'email': data['email'],
            'type': 'successfully',
        }
        return Response(response, status=status_code)





class UpdateAccountInfo(APIView): 
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        data = request.data
        user = request.user
        if user.check_password(data['cur_pwd']):
            user.set_password(data['pwd'])
            user.save()
            status_code = status.HTTP_200_OK
            response = {
                'status code': status_code,
                'success': 'True',
            }
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'status code': status_code,
                'success': 'False'
            }
        return Response(response, status=status_code)





Session_key = ""
class UserLoginView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data= request.data)
        serializer.is_valid(raise_exception=True)

        s = SessionStore()
        s['user_mail'] = serializer.data['email']
        s.create()
        global Session_key
        Session_key = s.session_key

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
            'type': 'successfully',
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
            'type': 'successfully',
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
                'type': 'successfully',
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
            'type': 'successfully',
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
            if(data['mesurment_method'] == 1): 
                method.click_link = ""
            if(data['mesurment_method'] == 2): 
                method.click_link = "http://18.181.122.179/app/basic/counts/?id="
            if(data['mesurment_method'] == 3): 
                method.click_link = str(user.corporate_homepage) + "/dmclicked.php/?id="
            method.save()

        else:
            MesurmentMethodSettingModel.objects.create(
                mesurment_method = data['mesurment_method'], 
                user = user       
            )

        register_statu = 1 
        if(user.corporate_country == None or \
            user.corporate_prefecture == None or \
                user.corporate_city == None or \
                    user.corporate_address == None):
                    
            register_statu = 0

        status_code = status.HTTP_201_CREATED
        response = {
            'success': 'True',
            'status code': status_code,
            'register_statu': register_statu,
            'type': 'successfully',
        }
        return Response(response, status=status_code)



class Getmesurmentmethodsetting(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request): 
        user = request.user 

        method = MesurmentMethodSettingModel.objects.filter(Q(user=user)).first()
        
        if method :
            status_code = status.HTTP_200_OK
            response = {
                'success': 'True',
                'method':method.mesurment_method,
                'corporate_homepage':user.corporate_homepage,
                'status code': status_code,
                'type': 'successfully',
            }
            return Response(response, status=status_code)

        else: 
            status_code = status.HTTP_200_OK
            response = {
                'success': 'True',
                'method': 1,
                'corporate_homepage':user.corporate_homepage,
                'status code': status_code,
                'type': 'successfully',
            }
            return Response(response, status=status_code)




class DMtextSet(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request): 
        user = request.user
        data = request.data  

        data['text1000'] = data['text1000'].replace("{company-type}", str(user.company_type))
        data['text1000'] = data['text1000'].replace("{client-frigana}", str(user.corporate_furigana))
        data['text1000'] = data['text1000'].replace("{client-postcode}", str(user.corporate_zipcode))
        data['text1000'] = data['text1000'].replace("{client-country}", str(user.corporate_country))
        data['text1000'] = data['text1000'].replace("{client-prefecture}", str(user.corporate_prefecture))
        data['text1000'] = data['text1000'].replace("{client-city}", str(user.corporate_city))
        data['text1000'] = data['text1000'].replace("{client-address}", str(user.corporate_address))
        data['text1000'] = data['text1000'].replace("{client-buildingname}", str(user.corporate_building_name))
        data['text1000'] = data['text1000'].replace("{client-roomnumber}", str(user.corporate_address_room_number))
        data['text1000'] = data['text1000'].replace("{client-establishdate}", str(user.corporate_estable_date))
        data['text1000'] = data['text1000'].replace("{client-phone}", str(user.corporate_phone))
        data['text1000'] = data['text1000'].replace("{client-fax}", str(user.corporate_fax))
        data['text1000'] = data['text1000'].replace("{client-mailaddress}", str(user.corporate_mail))
        data['text1000'] = data['text1000'].replace("{client-homepage}", str(user.corporate_homepage))
        data['text1000'] = data['text1000'].replace("{staff-firstname}", str(user.firstname_of_charger))
        data['text1000'] = data['text1000'].replace("{staff-lastname}", str(user.lastname_of_charger))
        data['text1000'] = data['text1000'].replace("{staff-friganafirstname}", str(user.firstname_of_charger_firagana))
        data['text1000'] = data['text1000'].replace("{staff-friganalastname}", str(user.lastname_of_charger_firagana))
        data['text1000'] = data['text1000'].replace("{staff-address}", str(user.charger_prefecture))
        data['text1000'] = data['text1000'].replace("{staff-phone}", str(user.charger_phone))

        data['text500'] = data['text500'].replace("{company-type}", str(user.company_type))
        data['text500'] = data['text500'].replace("{client-frigana}", str(user.corporate_furigana))
        data['text500'] = data['text500'].replace("{client-postcode}", str(user.corporate_zipcode))
        data['text500'] = data['text500'].replace("{client-country}", str(user.corporate_country))
        data['text500'] = data['text500'].replace("{client-prefecture}", str(user.corporate_prefecture))
        data['text500'] = data['text500'].replace("{client-city}", str(user.corporate_city))
        data['text500'] = data['text500'].replace("{client-address}", str(user.corporate_address))
        data['text500'] = data['text500'].replace("{client-buildingname}", str(user.corporate_building_name))
        data['text500'] = data['text500'].replace("{client-roomnumber}", str(user.corporate_address_room_number))
        data['text500'] = data['text500'].replace("{client-establishdate}", str(user.corporate_estable_date))
        data['text500'] = data['text500'].replace("{client-phone}", str(user.corporate_phone))
        data['text500'] = data['text500'].replace("{client-fax}", str(user.corporate_fax))
        data['text500'] = data['text500'].replace("{client-mailaddress}", str(user.corporate_mail))
        data['text500'] = data['text500'].replace("{client-homepage}", str(user.corporate_homepage))
        data['text500'] = data['text500'].replace("{staff-firstname}", str(user.firstname_of_charger))
        data['text500'] = data['text500'].replace("{staff-lastname}", str(user.lastname_of_charger))
        data['text500'] = data['text500'].replace("{staff-friganafirstname}", str(user.firstname_of_charger_firagana))
        data['text500'] = data['text500'].replace("{staff-friganalastname}", str(user.lastname_of_charger_firagana))
        data['text500'] = data['text500'].replace("{staff-address}", str(user.charger_prefecture))
        data['text500'] = data['text500'].replace("{staff-phone}", str(user.charger_phone))

        data['text250'] = data['text250'].replace("{company-type}", str(user.company_type))
        data['text250'] = data['text250'].replace("{client-frigana}", str(user.corporate_furigana))
        data['text250'] = data['text250'].replace("{client-postcode}", str(user.corporate_zipcode))
        data['text250'] = data['text250'].replace("{client-country}", str(user.corporate_country))
        data['text250'] = data['text250'].replace("{client-prefecture}", str(user.corporate_prefecture))
        data['text250'] = data['text250'].replace("{client-city}", str(user.corporate_city))
        data['text250'] = data['text250'].replace("{client-address}", str(user.corporate_address))
        data['text250'] = data['text250'].replace("{client-buildingname}", str(user.corporate_building_name))
        data['text250'] = data['text250'].replace("{client-roomnumber}", str(user.corporate_address_room_number))
        data['text250'] = data['text250'].replace("{client-establishdate}", str(user.corporate_estable_date))
        data['text250'] = data['text250'].replace("{client-phone}", str(user.corporate_phone))
        data['text250'] = data['text250'].replace("{client-fax}", str(user.corporate_fax))
        data['text250'] = data['text250'].replace("{client-mailaddress}", str(user.corporate_mail))
        data['text250'] = data['text250'].replace("{client-homepage}", str(user.corporate_homepage))
        data['text250'] = data['text250'].replace("{staff-firstname}", str(user.firstname_of_charger))
        data['text250'] = data['text250'].replace("{staff-lastname}", str(user.lastname_of_charger))
        data['text250'] = data['text250'].replace("{staff-friganafirstname}", str(user.firstname_of_charger_firagana))
        data['text250'] = data['text250'].replace("{staff-friganalastname}", str(user.lastname_of_charger_firagana))
        data['text250'] = data['text250'].replace("{staff-address}", str(user.charger_prefecture))
        data['text250'] = data['text250'].replace("{staff-phone}", str(user.charger_phone))

        data['text100'] = data['text100'].replace("{company-type}", str(user.company_type))
        data['text100'] = data['text100'].replace("{client-frigana}", str(user.corporate_furigana))
        data['text100'] = data['text100'].replace("{client-postcode}", str(user.corporate_zipcode))
        data['text100'] = data['text100'].replace("{client-country}", str(user.corporate_country))
        data['text100'] = data['text100'].replace("{client-prefecture}", str(user.corporate_prefecture))
        data['text100'] = data['text100'].replace("{client-city}", str(user.corporate_city))
        data['text100'] = data['text100'].replace("{client-address}", str(user.corporate_address))
        data['text100'] = data['text100'].replace("{client-buildingname}", str(user.corporate_building_name))
        data['text100'] = data['text100'].replace("{client-roomnumber}", str(user.corporate_address_room_number))
        data['text100'] = data['text100'].replace("{client-establishdate}", str(user.corporate_estable_date))
        data['text100'] = data['text100'].replace("{client-phone}", str(user.corporate_phone))
        data['text100'] = data['text100'].replace("{client-fax}", str(user.corporate_fax))
        data['text100'] = data['text100'].replace("{client-mailaddress}", str(user.corporate_mail))
        data['text100'] = data['text100'].replace("{client-homepage}", str(user.corporate_homepage))
        data['text100'] = data['text100'].replace("{staff-firstname}", str(user.firstname_of_charger))
        data['text100'] = data['text100'].replace("{staff-lastname}", str(user.lastname_of_charger))
        data['text100'] = data['text100'].replace("{staff-friganafirstname}", str(user.firstname_of_charger_firagana))
        data['text100'] = data['text100'].replace("{staff-friganalastname}", str(user.lastname_of_charger_firagana))
        data['text100'] = data['text100'].replace("{staff-address}", str(user.charger_prefecture))
        data['text100'] = data['text100'].replace("{staff-phone}", str(user.charger_phone)) 

        DMtextSetModel.objects.create(
            title50 = data['title50'], 
            title25 = data['title25'], 
            title10 = data['title10'], 
            text1000 = data['text1000'], 
            text500 = data['text500'], 
            text250 = data['text250'], 
            text100 = data['text100'], 
            register_date = datetime.now(),
            user = user       
        )

        status_code = status.HTTP_201_CREATED
        response = {
            'success': 'True',
            'status code': status_code,
            'type': 'successfully',
        }
        return Response(response, status=status_code)



class GetDMAlltextdata(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request): 
        user = request.user 
        
        userdata = []
        if(user.coporate_name != None):
            userdata.append({"data": user.coporate_name, "name":"法人名", "mark":"client-name"})        
        if(user.company_type != None):
            userdata.append({"data": user.company_type, "name":"会社の種類", "mark":"company-type"})
        if(user.corporate_furigana != None):
            userdata.append({"data": user.corporate_furigana, "name":"法人ふりがな", "mark":"client-frigana"})
        if(user.corporate_zipcode != None):
            userdata.append({"data": user.corporate_zipcode, "name":"法人郵便番号", "mark":"client-postcode"})
        if(user.corporate_country != None):
            userdata.append({"data": user.corporate_country, "name":"法人国", "mark":"client-country"})
        if(user.corporate_prefecture != None):
            userdata.append({"data": user.corporate_prefecture, "name":"法人都道府県", "mark":"client-prefecture"})
        if(user.corporate_city != None):
            userdata.append({"data": user.corporate_city, "name":"法人市区町村", "mark":"client-city"})
        if(user.corporate_address != None):
            userdata.append({"data": user.corporate_address, "name":"法人住所枝番", "mark":"client-address"})
        if(user.corporate_building_name != None):
            userdata.append({"data": user.corporate_building_name, "name":"法人住所建物名", "mark":"client-buildingname"})
        if(user.corporate_address_room_number != None):
            userdata.append({"data": user.corporate_address_room_number, "name":"法人住所部屋番号", "mark":"client-roomnumber"})
        if(user.corporate_estable_date != None):
            userdata.append({"data": user.corporate_estable_date, "name":"法人住設立年", "mark":"client-establishdate"})
        if(user.corporate_phone != None):
            userdata.append({"data": user.corporate_phone, "name":"法人電話番号", "mark":"client-phone"})
        if(user.corporate_fax != None):
            userdata.append({"data": user.corporate_fax, "name":"法人FAX番号", "mark":"client-fax"})
        if(user.corporate_mail != None):
            userdata.append({"data": user.corporate_mail, "name":"法人メールアドレス", "mark":"client-mailaddress"})
        if(user.corporate_homepage != None):
            userdata.append({"data": user.corporate_homepage, "name":"法人ホームページ", "mark":"client-homepage"})
        if(user.firstname_of_charger != None):
            userdata.append({"data": user.firstname_of_charger, "name":"担当者姓", "mark":"staff-firstname"})
        if(user.lastname_of_charger != None):
            userdata.append({"data": user.lastname_of_charger, "name":"担当者名", "mark":"staff-lastname"})
        if(user.firstname_of_charger_firagana != None):
            userdata.append({"data": user.firstname_of_charger_firagana, "name":"担当者姓ふりがな", "mark":"staff-friganafirstname"})
        if(user.lastname_of_charger_firagana != None):
            userdata.append({"data": user.lastname_of_charger_firagana, "name":"担当者名ふりがな", "mark":"staff-friganalastname"})
        if(user.charger_prefecture != None):
            userdata.append({"data": user.charger_prefecture, "name":"担当者部署", "mark":"staff-address"})
        if(user.charger_phone != None):
            userdata.append({"data": user.charger_phone, "name":"担当電話番号", "mark":"staff-phone"})
         
        alldmtext = DMtextSetModel.objects.filter(Q(user=user)).values('pk', 'title50', 'title25', 'title10', 'text1000', 'text500', 'text250', 'text100', 'register_date', 'recent_send_date', 'sent_count', 'click_rate', 'total_count', 'average_count' )
        
        status_code = status.HTTP_200_OK
        response = {
            'success':          'True',
            'dmdata':           alldmtext,
            'userdata':         userdata,
            'status code':      status_code,
            'type':             'successfully',
        }
        return Response(response, status=status_code)




class Copydmtextrows(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request): 
        user = request.user 
        d = request.data 
         
        DMtextSetModel.objects.create(
            title50 = d['title50'], 
            title25 = d['title25'], 
            title10 = d['title10'], 
            text1000 = d['text1000'], 
            text500 = d['text500'], 
            text250 = d['text250'], 
            text100 = d['text100'], 
            register_date = datetime.now(),
            user = user 
        )
        
        status_code = status.HTTP_200_OK
        response = {
            'success': 'True', 
            'status code': status_code,
            'type': 'successfully',
        }

        return Response(response, status=status_code)



class Deletedmtextrows(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request): 
        user = request.user 
        data = request.data 

        dmtextrow = DMtextSetModel.objects.filter(Q(id = data['tableID']) & Q(user = user)).first() 
        dmtextrow.delete()           
        
        status_code = status.HTTP_204_NO_CONTENT
        response = {
            'success': 'True', 
            'status code': status_code,
            'type': 'successfully',
        }

        return Response(response, status=status_code)




class EditedDmtextSave(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request): 
        user = request.user 
        data = request.data   
        data['text1000'] = data['text1000'].replace("{company-type}", str(user.company_type))
        data['text1000'] = data['text1000'].replace("{client-frigana}", str(user.corporate_furigana))
        data['text1000'] = data['text1000'].replace("{client-postcode}", str(user.corporate_zipcode))
        data['text1000'] = data['text1000'].replace("{client-country}", str(user.corporate_country))
        data['text1000'] = data['text1000'].replace("{client-prefecture}", str(user.corporate_prefecture))
        data['text1000'] = data['text1000'].replace("{client-city}", str(user.corporate_city))
        data['text1000'] = data['text1000'].replace("{client-address}", str(user.corporate_address))
        data['text1000'] = data['text1000'].replace("{client-buildingname}", str(user.corporate_building_name))
        data['text1000'] = data['text1000'].replace("{client-roomnumber}", str(user.corporate_address_room_number))
        data['text1000'] = data['text1000'].replace("{client-establishdate}", str(user.corporate_estable_date))
        data['text1000'] = data['text1000'].replace("{client-phone}", str(user.corporate_phone))
        data['text1000'] = data['text1000'].replace("{client-fax}", str(user.corporate_fax))
        data['text1000'] = data['text1000'].replace("{client-mailaddress}", str(user.corporate_mail))
        data['text1000'] = data['text1000'].replace("{client-homepage}", str(user.corporate_homepage))
        data['text1000'] = data['text1000'].replace("{staff-firstname}", str(user.firstname_of_charger))
        data['text1000'] = data['text1000'].replace("{staff-lastname}", str(user.lastname_of_charger))
        data['text1000'] = data['text1000'].replace("{staff-friganafirstname}", str(user.firstname_of_charger_firagana))
        data['text1000'] = data['text1000'].replace("{staff-friganalastname}", str(user.lastname_of_charger_firagana))
        data['text1000'] = data['text1000'].replace("{staff-address}", str(user.charger_prefecture))
        data['text1000'] = data['text1000'].replace("{staff-phone}", str(user.charger_phone))

        data['text500'] = data['text500'].replace("{company-type}", str(user.company_type))
        data['text500'] = data['text500'].replace("{client-frigana}", str(user.corporate_furigana))
        data['text500'] = data['text500'].replace("{client-postcode}", str(user.corporate_zipcode))
        data['text500'] = data['text500'].replace("{client-country}", str(user.corporate_country))
        data['text500'] = data['text500'].replace("{client-prefecture}", str(user.corporate_prefecture))
        data['text500'] = data['text500'].replace("{client-city}", str(user.corporate_city))
        data['text500'] = data['text500'].replace("{client-address}", str(user.corporate_address))
        data['text500'] = data['text500'].replace("{client-buildingname}", str(user.corporate_building_name))
        data['text500'] = data['text500'].replace("{client-roomnumber}", str(user.corporate_address_room_number))
        data['text500'] = data['text500'].replace("{client-establishdate}", str(user.corporate_estable_date))
        data['text500'] = data['text500'].replace("{client-phone}", str(user.corporate_phone))
        data['text500'] = data['text500'].replace("{client-fax}", str(user.corporate_fax))
        data['text500'] = data['text500'].replace("{client-mailaddress}", str(user.corporate_mail))
        data['text500'] = data['text500'].replace("{client-homepage}", str(user.corporate_homepage))
        data['text500'] = data['text500'].replace("{staff-firstname}", str(user.firstname_of_charger))
        data['text500'] = data['text500'].replace("{staff-lastname}", str(user.lastname_of_charger))
        data['text500'] = data['text500'].replace("{staff-friganafirstname}", str(user.firstname_of_charger_firagana))
        data['text500'] = data['text500'].replace("{staff-friganalastname}", str(user.lastname_of_charger_firagana))
        data['text500'] = data['text500'].replace("{staff-address}", str(user.charger_prefecture))
        data['text500'] = data['text500'].replace("{staff-phone}", str(user.charger_phone))

        data['text250'] = data['text250'].replace("{company-type}", str(user.company_type))
        data['text250'] = data['text250'].replace("{client-frigana}", str(user.corporate_furigana))
        data['text250'] = data['text250'].replace("{client-postcode}", str(user.corporate_zipcode))
        data['text250'] = data['text250'].replace("{client-country}", str(user.corporate_country))
        data['text250'] = data['text250'].replace("{client-prefecture}", str(user.corporate_prefecture))
        data['text250'] = data['text250'].replace("{client-city}", str(user.corporate_city))
        data['text250'] = data['text250'].replace("{client-address}", str(user.corporate_address))
        data['text250'] = data['text250'].replace("{client-buildingname}", str(user.corporate_building_name))
        data['text250'] = data['text250'].replace("{client-roomnumber}", str(user.corporate_address_room_number))
        data['text250'] = data['text250'].replace("{client-establishdate}", str(user.corporate_estable_date))
        data['text250'] = data['text250'].replace("{client-phone}", str(user.corporate_phone))
        data['text250'] = data['text250'].replace("{client-fax}", str(user.corporate_fax))
        data['text250'] = data['text250'].replace("{client-mailaddress}", str(user.corporate_mail))
        data['text250'] = data['text250'].replace("{client-homepage}", str(user.corporate_homepage))
        data['text250'] = data['text250'].replace("{staff-firstname}", str(user.firstname_of_charger))
        data['text250'] = data['text250'].replace("{staff-lastname}", str(user.lastname_of_charger))
        data['text250'] = data['text250'].replace("{staff-friganafirstname}", str(user.firstname_of_charger_firagana))
        data['text250'] = data['text250'].replace("{staff-friganalastname}", str(user.lastname_of_charger_firagana))
        data['text250'] = data['text250'].replace("{staff-address}", str(user.charger_prefecture))
        data['text250'] = data['text250'].replace("{staff-phone}", str(user.charger_phone))

        data['text100'] = data['text100'].replace("{company-type}", str(user.company_type))
        data['text100'] = data['text100'].replace("{client-frigana}", str(user.corporate_furigana))
        data['text100'] = data['text100'].replace("{client-postcode}", str(user.corporate_zipcode))
        data['text100'] = data['text100'].replace("{client-country}", str(user.corporate_country))
        data['text100'] = data['text100'].replace("{client-prefecture}", str(user.corporate_prefecture))
        data['text100'] = data['text100'].replace("{client-city}", str(user.corporate_city))
        data['text100'] = data['text100'].replace("{client-address}", str(user.corporate_address))
        data['text100'] = data['text100'].replace("{client-buildingname}", str(user.corporate_building_name))
        data['text100'] = data['text100'].replace("{client-roomnumber}", str(user.corporate_address_room_number))
        data['text100'] = data['text100'].replace("{client-establishdate}", str(user.corporate_estable_date))
        data['text100'] = data['text100'].replace("{client-phone}", str(user.corporate_phone))
        data['text100'] = data['text100'].replace("{client-fax}", str(user.corporate_fax))
        data['text100'] = data['text100'].replace("{client-mailaddress}", str(user.corporate_mail))
        data['text100'] = data['text100'].replace("{client-homepage}", str(user.corporate_homepage))
        data['text100'] = data['text100'].replace("{staff-firstname}", str(user.firstname_of_charger))
        data['text100'] = data['text100'].replace("{staff-lastname}", str(user.lastname_of_charger))
        data['text100'] = data['text100'].replace("{staff-friganafirstname}", str(user.firstname_of_charger_firagana))
        data['text100'] = data['text100'].replace("{staff-friganalastname}", str(user.lastname_of_charger_firagana))
        data['text100'] = data['text100'].replace("{staff-address}", str(user.charger_prefecture))
        data['text100'] = data['text100'].replace("{staff-phone}", str(user.charger_phone)) 

         
        dmtextrow = DMtextSetModel.objects.filter(Q(id = data['tableID']) & Q(user = user)).first() 
        dmtextrow.title50 = data['title50']         
        dmtextrow.title25 = data['title25']         
        dmtextrow.title10 = data['title10']         
        dmtextrow.text1000 = data['text1000']         
        dmtextrow.text500 = data['text500']         
        dmtextrow.text250 = data['text250']         
        dmtextrow.text100 = data['text100']   
        dmtextrow.save()           
         
        status_code = status.HTTP_200_OK
        response = {
            'success': 'True', 
            'status code': status_code,
            'type': 'successfully',
        }
        return Response(response, status=status_code)






class GetAllDMGroupData(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request): 
        user = request.user 

        data = DMGroupModel.objects.filter(Q(user=user)).values('pk', 'title', 'subjectcount' )
        register_statu = 1 
        if(user.corporate_country == None or \
            user.corporate_prefecture == None or \
                user.corporate_city == None or \
                    user.corporate_address == None):
            register_statu = 0

        isPayed = False
        if(user.paydate != None and user.initial_pay_statu == 1):
            isPayed = True
        status_code = status.HTTP_200_OK
        response = {
            'success': 'True',
            'data': data,
            'isPayed': isPayed, 
            'register_statu': register_statu,
            'status code': status_code,
            'type': 'successfully',
        }

        return Response(response, status=status_code)




class SaveAllDMGroupData(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request): 
        user = request.user 
        data = request.data   
        for d in data:
            if (d['pk'] == ''):                
                DMGroupModel.objects.create(
                    title = d['title'], 
                    user = user
                )  

            else :
                dmgroups = DMGroupModel.objects.filter(Q(id = d['pk'])).first()
                listscount = PerDMGroupDmListModel.objects.filter(Q(dmgroup = dmgroups)).count()                
                dmgroups.title = d['title'] 
                dmgroups.subjectcount = listscount
                dmgroups.save() 
         
        data = DMGroupModel.objects.filter(Q(user=user)).values('pk', 'title', 'subjectcount' )

        status_code = status.HTTP_200_OK
        response = {
            'success': 'True', 
            'data': data,
            'status code': status_code,
            'type': 'successfully',
        }
        return Response(response, status=status_code)





class Deletdmgroup(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request): 
        user = request.user 
        data = request.data
        resdata = ""        
        for d in data:
            if(d['pk'] != ''):
                dmgroup = DMGroupModel.objects.filter(Q(id = d['pk']) & Q(user = user)).first() 
                pergroup_list = PerDMGroupDmListModel.objects.filter(Q(dmgroup = dmgroup.id) & Q(user = user)) 
                dmgroup.delete()    
                pergroup_list.delete()       
                resdata = "ok"
            
            else:
                resdata = "doedit"
                

        status_code = status.HTTP_204_NO_CONTENT
        response = {
            'success': 'True', 
            'data': resdata,
            'status code': status_code,
            'type': 'successfully',
        }

        return Response(response, status=status_code)


class CsvImport(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        user = request.user 
        csvfile = request.FILES.get('csv', '') 
        fs = FileSystemStorage()
        filename = fs.save("csvdmlist", csvfile)
        filepath = fs.url(filename) 
        empexceldata = pd.read_csv("."+filepath, encoding="shift-jis")
         
        responseData = []
        i = 1
        for dbframe in empexceldata.itertuples():  

            cname = ""
            cmailaddress = ""
            ccontact_url = ""
            csite_url = ""
            cphone_num = ""

            if(str(dbframe.企業名) != "nan"):
                cname = dbframe.企業名
            if(str(dbframe.メールアドレス) != "nan"):
                cmailaddress = dbframe.メールアドレス
            if(str(dbframe.問合せフォームURL) != "nan"):
                ccontact_url = dbframe.問合せフォームURL
            if(str(dbframe.サイトURL) != "nan"):
                csite_url = dbframe.サイトURL
            if(str(dbframe.電話番号) != "nan"):
                cphone_num = dbframe.電話番号

            

            responseData.append({
                "id":i,
                "name":cname, 
                "mailaddress":cmailaddress,
                "contact_url":ccontact_url,
                "site_url":csite_url,
                "phone_num":cphone_num,
                "auto_manual":"CSV", 
            }) 

            i = i+1 
 

        
        empexceldataPath = os.path.join(settings.MEDIA_ROOT, filename)
        os.remove(empexceldataPath)
        
        return Response(json.dumps({"data": responseData}))





class Stopcsvimport(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        user = request.user 
        csvfile = request.FILES.get('csv', '') 
        fs = FileSystemStorage()
        filename = fs.save(csvfile.name, csvfile)
        filepath = fs.url(filename)
        empexceldata = pd.read_excel("."+filepath)
        
        responseData = [] 
        for dbframe in empexceldata.itertuples():  
            
            name = dbframe.企業名          
            mailaddress = dbframe.メール          
            contact_url = dbframe.お問合せフォームURL          
            site_url = dbframe.URL          
            phone_num = dbframe.郵便番号  

            if(name == 0):
                name = None  
            if(mailaddress == 0):
                mailaddress = None  
            if(contact_url == 0):
                contact_url = None  
            if(site_url == 0):
                site_url = None  
            if(phone_num == 0):
                phone_num = None   
 
            responseData.append({ 
                "corporate_name":name, 
                "mailaddress":mailaddress,
                "contact_url":contact_url,
                "site_url":site_url,
                "phone":phone_num, 
            })            


        empexceldataPath = os.path.join(settings.MEDIA_ROOT, filename)
        os.remove(empexceldataPath)

        for d in responseData: 
            StopLinkSettingModel.objects.create(
                name = d['corporate_name'],
                mailaddress = d['mailaddress'],
                contact_url = d['contact_url'],
                site_url = d['site_url'],
                phone_num = d['phone'],
                auto_manual =  "CSV", 
                user = user,            
            )

        resdata = StopLinkSettingModel.objects.filter(Q(user=user)).values('pk', 'name', 'mailaddress', 'contact_url', 'site_url', 'phone_num', 'auto_manual' )
        
        status_code = status.HTTP_201_CREATED
        response = {
            'success': 'True',
            'status code': status_code,
            'data':resdata,
            'type': 'successfully',
        }
        return Response(response, status=status_code)




class Deletestoplist(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request): 
        user = request.user 
        data = request.data 
        
        if(data['row'] == 1):
            deletelist = StopLinkSettingModel.objects.filter(Q(id=data['data']['tb_id'])).first()
            deletelist.delete()

        if(data['row'] == 2):
            for d in data['data']:
                deletelist = StopLinkSettingModel.objects.filter(Q(id=d['tb_id'])).first()
                deletelist.delete()

        resdata = StopLinkSettingModel.objects.filter(Q(user=user)).values('pk', 'name', 'mailaddress', 'contact_url', 'site_url', 'phone_num', 'auto_manual' )
        
        status_code = status.HTTP_201_CREATED
        response = {
            'success': 'True',
            'status code': status_code,
            'data':resdata,
            'type': 'successfully',
        }
        return Response(response, status=status_code)


class DMlistsSave(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request): 
        user = request.user 
        data = request.data 
        savemethod = data['savemethod']
        dmgroup = None
        if(savemethod == 1):
            for d in data['data']:
                dmgroup = DMGroupModel.objects.filter(Q(id = d['dmgropID'])).first()
                if (d['tb_id'] == ''):                
                    PerDMGroupDmListModel.objects.create(
                        name = d['name'], 
                        mailaddress = d['mailaddress'], 
                        contact_url = d['contact_url'], 
                        site_url = d['site_url'], 
                        phone_num = d['phone_num'], 
                        auto_manual = d['auto_manual'], 
                        dmgroup = dmgroup, 
                        user = user
                    )  

                else :
                    listscount = PerDMGroupDmListModel.objects.filter(Q(id = d['tb_id'])).first()             
                    listscount.name = d['name']
                    listscount.mailaddress = d['mailaddress']
                    listscount.contact_url = d['contact_url']
                    listscount.site_url = d['site_url']
                    listscount.phone_num = d['phone_num']
                    listscount.auto_manual = d['auto_manual']
                    listscount.save() 

        else:
            for d in data['data']:
                dmgroup = DMGroupModel.objects.filter(Q(id = d['dmgropID'])).first()
                listscounts = PerDMGroupDmListModel.objects.filter(Q(dmgroup = dmgroup))                
                for listscount in listscounts:
                    listscount.delete()

            for d in data['data']:           
                dmgroup = DMGroupModel.objects.filter(Q(id = d['dmgropID'])).first()     
                PerDMGroupDmListModel.objects.create(
                    name = d['name'], 
                    mailaddress = d['mailaddress'], 
                    contact_url = d['contact_url'], 
                    site_url = d['site_url'], 
                    phone_num = d['phone_num'], 
                    auto_manual = d['auto_manual'], 
                    dmgroup = dmgroup, 
                    user = user
                ) 
                
        resdata = PerDMGroupDmListModel.objects.filter(Q(dmgroup=dmgroup)).values('pk', 'name', 'mailaddress', 'contact_url', 'site_url', 'phone_num', 'auto_manual' )
 
        status_code = status.HTTP_200_OK
        response = {
            'success': 'True', 
            'status code': status_code,
            'data':resdata,
            'type': 'successfully',
        }
        return Response(response, status=status_code)





class GetAllDMlists(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request): 
        user = request.user 
        data = request.data   
        dmgroup = DMGroupModel.objects.filter(Q(id = data['id'])).first()         
        resdata = PerDMGroupDmListModel.objects.filter(Q(dmgroup=dmgroup)).values('pk', 'name', 'mailaddress', 'contact_url', 'site_url', 'phone_num', 'auto_manual' )

        status_code = status.HTTP_200_OK
        response = {
            'success': 'True', 
            'status code': status_code,
            'data':resdata,
            'izanagi_list':user.option_price,
            'type': 'successfully',
        }
        return Response(response, status=status_code)




class GetAllStoplists(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request): 
        user = request.user         
        resdata = StopLinkSettingModel.objects.filter(Q(user=user)).values('pk', 'name', 'mailaddress', 'contact_url', 'site_url', 'phone_num', 'auto_manual' )

        status_code = status.HTTP_200_OK
        response = {
            'success': 'True', 
            'status code': status_code,
            'data':resdata,
            'type': 'successfully',
        }
        return Response(response, status=status_code)



class GetallStatus(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request): 
        user = request.user         
        resdata = DMSendStatusModel.objects.filter(Q(user=user)).values('pk', 'data', 'text_option', 'textpattern1', 'textpattern2', 'status')

        send_result = []

        for d in resdata:
            datas           = eval(d['data'])
            textpattern1s   = eval(d['textpattern1'])    
            textpattern2s   = eval(d['textpattern2'])    

            send_result.append({"data":datas, "textpattern1s":textpattern1s, "textpattern2s": textpattern2s, "text_option": d['text_option'], "status": d['status'], "pk":d['pk']})

        status_code = status.HTTP_200_OK
        response = {
            'success': 'True', 
            'status code': status_code,
            'data':send_result,
            'type': 'successfully',
        }
        return Response(response, status=status_code)




class GetallUsers(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request): 
        user = request.user     

        users = User.objects.filter().values('pk', 'email', 'password', 'coporate_name', 'corporate_mail', 'firstname_of_charger', 'lastname_of_charger', 'charger_phone')
         
        status_code = status.HTTP_200_OK
        response = {
            'success': 'True', 
            'status code': status_code,
            'data':users,
            'type': 'successfully',
        }
        return Response(response, status=status_code)





class Deletedmlists(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request): 
        data = request.data 
         
        if(data['rownum'] == 1):
            list = PerDMGroupDmListModel.objects.filter(Q(id = data['requestData']['tb_id'])).first()  
            list.delete()  

        else:
            for d in data['requestData']:
                list = PerDMGroupDmListModel.objects.filter(Q(id = d['tb_id'])).first()  
                list.delete()  
        
        status_code = status.HTTP_204_NO_CONTENT
        response = {
            'success': 'True', 
            'status code': status_code,
            'type': 'successfully',
        }

        return Response(response, status=status_code)




class SaveEditedListdata(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request): 
        user = request.user 
        data = request.data   
        
        if(data['tb_id'] == ''):
            dmgroup = DMGroupModel.objects.filter(Q(id = data['dmID'])).first()
            PerDMGroupDmListModel.objects.create(
                name = data['name'], 
                mailaddress = data['mailaddress'], 
                contact_url = data['contact_url'], 
                site_url = data['site_url'], 
                phone_num = data['phone_num'], 
                auto_manual = data['editauto_manual'], 
                dmgroup = dmgroup, 
                user = user
            )
        
        else:
            list = PerDMGroupDmListModel.objects.filter(Q(id = data['tb_id'])).first() 
            list.name = data['name']
            list.mailaddress = data['mailaddress']
            list.contact_url = data['contact_url']
            list.site_url = data['site_url']
            list.phone_num = data['phone_num']
            list.save() 

        dmgroup = DMGroupModel.objects.filter(Q(id = data['dmID'])).first()         
        resdata = PerDMGroupDmListModel.objects.filter(Q(dmgroup=dmgroup)).values('pk', 'name', 'mailaddress', 'contact_url', 'site_url', 'phone_num', 'auto_manual' )

        status_code = status.HTTP_200_OK
        response = {
            'success': 'True', 
            'status code': status_code,
            'data':resdata,
            'type': 'successfully',
        }
        return Response(response, status=status_code)





class AddDMLists(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):        
        user = request.user
        data = request.data 

        dmgroup = DMGroupModel.objects.filter(Q(id = data['groupid'])).first() 
         
        if(data['method'] == '1'):            
            for d in data['data']:                  
                PerDMGroupDmListModel.objects.create(
                    name = d['corporate_name'],
                    mailaddress = d['mailaddress'],
                    contact_url = d['contact_url'],
                    site_url = d['site_url'],
                    phone_num = d['phone'],
                    auto_manual =  "手動", 
                    user = user,     
                    dmgroup = dmgroup,       
                )
        
        else:
            listscounts = PerDMGroupDmListModel.objects.filter(Q(dmgroup = dmgroup))                
            for listscount in listscounts:
                listscount.delete() 
            for d in data['data']: 
                PerDMGroupDmListModel.objects.create(
                    name = d['corporate_name'],
                    mailaddress = d['mailaddress'],
                    contact_url = d['contact_url'],
                    site_url = d['site_url'],
                    phone_num = d['phone'],
                    auto_manual =  "手動", 
                    user = user,     
                    dmgroup = dmgroup,       
                )

        status_code = status.HTTP_201_CREATED
        response = {
            'success': 'True',
            'status code': status_code,
            'type': 'successfully',
        }
        return Response(response, status=status_code) 




class GetGroupAndTextPattern(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request): 
        user = request.user 
        data = request.data   
        dmgroup = DMGroupModel.objects.filter(Q(id = data['id'])).first()         
        resdata = PerDMGroupDmListModel.objects.filter(Q(dmgroup = dmgroup)).values('pk', 'name', 'mailaddress', 'contact_url', 'site_url', 'phone_num', 'auto_manual' )
        textPatter = DMtextSetModel.objects.filter(Q(user = user)).values('pk', 'title50', 'title25', 'title10', 'text1000', 'text500', 'text250', 'text100', 'recent_send_date', 'sent_count', 'click_rate', 'total_count', 'average_count')
        method = MesurmentMethodSettingModel.objects.filter(Q(user=user)).first()
        textpattern_temp = []
         

        for tp in textPatter:
            link_url = ""
            if method and method.click_link:
                link_url = "\n\n\n" + method.click_link +str(tp['pk'])
            textpattern_temp.append({
                'pk':tp['pk'],
                'title50':tp['title50'],
                'title25':tp['title25'],
                'title10':tp['title10'],
                'text1000':tp['text1000'] + link_url,
                'text500':tp['text500'] + link_url,
                'text250':tp['text250'] + link_url,
                'text100':tp['text100'] + link_url,
                'recent_send_date':tp['recent_send_date'],
                'sent_count':tp['sent_count'],
                'click_rate':tp['click_rate'],
                'total_count':tp['total_count'],
                'average_count':tp['average_count'],
            })
 
        status_code = status.HTTP_200_OK
        response = {
            'success': 'True', 
            'status code': status_code,
            'data':resdata,
            'textpat': textpattern_temp,
            'type': 'successfully',
        }
        return Response(response, status=status_code)



interupt_flag = False
total_result  = []
process_count = 0
process_flag  = False

class GetFormData(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):  
        user            = request.user 
        data            = request.data 
        text_option     = data['text_option']
        tpat1           = data['tpat1']
        tpat2           = data['tpat2'] 

        browser         = Browser()
        browser.set_handle_equiv(False)
        browser.set_handle_robots(False)
        browser.addheaders = [('User-agent','Mozilla/5.0 (X11; Linux x86_64; rv:18.0)Gecko/20100101 Firefox/18.0 (compatible;)'),('Accept', '*/*')]   

        
        
        global interupt_flag, total_result, process_count, process_flag         
 
        if(text_option == 1): #---------------------配信文章を選択
            if(data['send_date'] == 1): #-----------送信日時の設定
                if(data['send_method'] == 1): #-----送信方法を選択
                    sendDMAutoMatic(data, user, tpat1)
                    while not process_flag: 
                        True

        if(text_option == 2): #---------------------配信文章を選択
            if(data['send_date'] == 1): #-----------送信日時の設定
                if(data['send_method'] == 1): #-----送信方法を選択
                    sendDMAutoMatic(data, user, tpat1)
                    while not process_flag:
                        True
                    sendDMAutoMatic(data, user, tpat2)
                    while not process_flag:
                        True

        
        if(data['send_date'] == 2): #-----------送信日時の設定                     
            for d in data['rows']:
                total_result.append({"status":"reservation", "data": d })                
            reserveTimer = th.Timer(180, checkSendingCondition)
            reserveTimer.start() 
        
        
        
        req_data = total_result
        total_result = []
        interupt_flag = False  

        timeTemp    = None
        reserTemp   = ""
        
        if(data['specific_date'] != None):
            reserTemp = data['specific_date']

        if(data['reservedDate'] != None): 
            timeTemp = datetime.strptime(data['reservedDate'], '%Y-%m-%d %H:%M:%S').date()

        for req_data_item in req_data: 
            
            resdata = PerDMGroupDmListModel.objects.filter(Q(id = req_data_item['data']['tb_id'])).first()
            resdata.last_sent_date = datetime.now()
            resdata.last_sent_user = user.firstname_of_charger + user.lastname_of_charger
            resdata.save()

            totalsendcount = user.total_send_count + len(req_data)
            user.total_send_count  = totalsendcount

            if(req_data_item['status'] == "fail"):
                user.total_send_faild_count = user.total_send_faild_count + 1

            if(req_data_item['status'] == "success"):
                user.total_send_success_count = user.total_send_success_count + 1

            if(req_data_item['status'] == "mail"):
                user.total_mail_send_count = user.total_mail_send_count + 1

            user.save()

            if (data['text_option'] == 1):
                dmtexttable = DMtextSetModel.objects.filter(Q(id = data['tpat1']['pk'])).first()
                if dmtexttable:
                    dmtexttable.total_count = dmtexttable.total_count + 1
                    if(req_data_item['status'] == "success" or req_data_item['status'] == "mail"):
                        dmtexttable.sent_count = dmtexttable.sent_count + 1
                dmtexttable.save()
            
            if (data['text_option'] == 2):
                dmtexttable = DMtextSetModel.objects.filter(Q(id = data['tpat2']['pk'])).first()
                dmtexttable.total_count = dmtexttable.total_count + 1
                if(req_data_item['status'] == "success" or req_data_item['status'] == "mail"):
                        dmtexttable.sent_count = dmtexttable.sent_count + 1
                dmtexttable = DMtextSetModel.objects.filter(Q(id = data['tpat1']['pk'])).first()
                dmtexttable.total_count = dmtexttable.total_count + 1
                if(req_data_item['status'] == "success" or req_data_item['status'] == "mail"):
                        dmtexttable.sent_count = dmtexttable.sent_count + 1
                dmtexttable.save()


            DMSendStatusModel.objects.create(
                data            = req_data_item['data'], 
                status          = req_data_item['status'],
                list_table_id   = req_data_item['data']['tb_id'],
                reserve_date    = timeTemp,
                specific_day    = reserTemp,
                textpattern1    = data['tpat1'],
                textpattern2    = data['tpat2'],
                text_option     = data['text_option'],
                user            = user       
            ) 

        if (data['text_option'] == 1):
            dmtexttable = DMtextSetModel.objects.filter(Q(id = data['tpat1']['pk'])).first()
            if dmtexttable:
                dmtexttable.recent_send_date = datetime.now() 
                dmtexttable.save()

        if (data['text_option'] == 2):
            dmtexttable = DMtextSetModel.objects.filter(Q(id = data['tpat2']['pk'])).first()
            if dmtexttable:
                dmtexttable.recent_send_date = datetime.now()
                dmtexttable.save()

            dmtexttable = DMtextSetModel.objects.filter(Q(id = data['tpat1']['pk'])).first()
            if dmtexttable:
                dmtexttable.recent_send_date = datetime.now()
                dmtexttable.save()


        status_code = status.HTTP_201_CREATED
        response = {
            'success': 'True', 
            'data': req_data,
            'status code': status_code, 
            'type': 'successfully'
        } 
        return Response(response, status=status_code)


 

class InterruptSendDM(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        global interupt_flag, total_result

        interupt_flag = True

        status_code = status.HTTP_201_CREATED
        response = {
            'success': 'True',  
            'data': total_result,
            'status code': status_code, 
            'type': 'successfully'
        } 

        return Response(response, status=status_code)

html_strs = []
html_str = ""
form_datas = []
all_form_datas = []
site_urls = []
site_url = ""

class ManualSendDM(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        user            = request.user 
        data            = request.data                   
        text_option     = data['text_option']
        tpattern = None 

        if(text_option == 1):
            tpattern           = data['tpat1']
            sendManuallySubFunction(data, user, tpattern)

        if(text_option == 2):
            tpattern           = data['tpat1']
            sendManuallySubFunction(data, user, tpattern)
            tpattern           = data['tpat2']
            sendManuallySubFunction(data, user, tpattern)        
         
        global html_strs, all_form_datas, site_urls
        
        hs =  html_strs
        fds = all_form_datas
        su = site_urls

        html_strs = []
        all_form_datas = []
        site_urls = []

         
        if len(all_form_datas) < 0:
            status_code = status.HTTP_201_CREATED
            response = {
                'success': 'false',  
                'data': hs,
                'form_datas':fds, 
                'link': su,
                'status code': status_code, 
                'type': 'successfully'
            }  

            return Response(response, status=status_code)
        else:
            status_code = status.HTTP_201_CREATED
            response = {
                'success': 'True',  
                'data': hs,
                'form_datas':fds, 
                'link': su,
                'status code': status_code, 
                'type': 'successfully'
            }  

            return Response(response, status=status_code)




class WebhookView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        webhook_secret = settings.STRIPE_WEBHOOK_KEY
        event_type = None 

        if webhook_secret:
            # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
            signature = request.headers.get('stripe-signature')
            try:
                event = stripe.Webhook.construct_event(
                    payload=request.body, sig_header=signature, secret=webhook_secret
                )
                data = event['data']
            except Exception as e:
                return Response(json.dumps({'status': 'failed'}))
            # Get the type of webhook event sent - used to check the status of PaymentIntents.
            event_type = event['type']
        else:
            data = request.data['data']
            event_type = request.data['type']
        data_object = data['object'] 
        print("============================")
        print(event_type)
        print("============================")
        if event_type == 'invoice.payment_succeeded': 
            if data_object['billing_reason'] == 'subscription_create':
                subscription_id = data_object['subscription']
                payment_intent_id = data_object['payment_intent']

                # Retrieve the payment intent used to pay the subscription
                payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)

                # Set the default payment method
                stripe.Subscription.modify(
                    subscription_id,
                    default_payment_method=payment_intent.payment_method
                )
            user = User.objects.filter(Q(customer_id = request.data['data']['object']['customer'])).first()
            if user: 
                now = datetime.today() 
                user.paydate = now
                user.expirydate =now + timedelta(days=30)
                user.save()

        if event_type == 'invoice.payment_failed':            
            user = User.objects.filter(Q(customer_id = request.data['data']['object']['customer'])).first()
            user.paydate = None
            user.expirydate = None  
            user.customer_id = None
            user.subscription_id = None
            user.save()
             
        if event_type == 'customer.subscription.deleted':
            user = User.objects.filter(Q(customer_id = request.data['data']['object']['customer'])).first()
            if user: 
                user.paydate = None
                user.expirydate = None 
                user.customer_id = None
                user.subscription_id = None
                user.save()

        if event_type == 'payment_intent.succeeded':   
            user = User.objects.filter(Q(initial_pay_id = request.data['data']['object']['id'])).first()
            if user: 
                user.initial_pay_statu = 1 
                user.save()

        return Response(json.dumps({'status': 'success'}))


class UserCreateSubscription(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        user = request.user 
        data = request.data

        stripe.api_key = settings.STRIPE_SECRET_KEY

        price_id = ""         

        if user.option_price:
            if(user.price_plan == 1):
                price_id = settings.ECO_ADD_LIST
            if(user.price_plan == 2):
                price_id = settings.STANDARD_ADD_LIST
            if(user.price_plan == 3):
                price_id = settings.PRO_ADD_LIST
            if(user.price_plan == 1):
                price_id = settings.ENTERPRIZE_ADD_LIST
        else:
            if(user.price_plan == 1):
                price_id = settings.ECO_PRICE_ID
            if(user.price_plan == 2):
                price_id = settings.STANDARD_PRICE_ID
            if(user.price_plan == 3):
                price_id = settings.PRO_PRICE_ID
            if(user.price_plan == 1):
                price_id = settings.ENTERPISE_PRICE_ID       

        
        try:
            customer = stripe.Customer.create(
                email = data['email']
            )
            user.customer_id = customer.id
            user.save()
            try:
                subscription = stripe.Subscription.create(
                    customer = customer.id,
                    items = [{
                        'price': price_id
                    }],
                    payment_behavior='default_incomplete',
                    expand=['latest_invoice.payment_intent'],
                )

                onetimeClientSecret = None
                isonetime = "no"

                if(user.initial_pay_statu == 0):
                    onetimepaymentIntents = stripe.PaymentIntent.create( 
                        amount = 150000,
                        currency = 'jpy',  
                        payment_method_types = ['card'], 
                    )                     
                    
                    onetimeClientSecret = onetimepaymentIntents.client_secret
                    isonetime = "ok"
                    user.initial_pay_id = onetimepaymentIntents.id
                    user.save()

                user.subscription_id = subscription.id
                user.save()
                
                status_code = status.HTTP_201_CREATED 
                response = {
                    'status': status_code,
                    'clientSecret': subscription.latest_invoice.payment_intent.client_secret,
                    'onetimeClientSecret': onetimeClientSecret,
                    'isonetime': isonetime
                } 

                return Response(response, status=status_code)
            except Exception as e: 
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e: 
            return Response(status=status.HTTP_400_BAD_REQUEST)







class UpdateSubscription(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        user = request.user 
        data = request.data

        stripe.api_key = settings.STRIPE_SECRET_KEY
        subscription = stripe.Subscription.retrieve(user.subscription_id)        

        price_id = None      
        optprice_flag = 0   

        if data['option_price'] == 30000:
            optprice_flag = 1
            if(data['plan'] == 1):
                price_id = settings.ECO_ADD_LIST
            if(data['plan'] == 2):
                price_id = settings.STANDARD_ADD_LIST
            if(data['plan'] == 3):
                price_id = settings.PRO_ADD_LIST
            if(data['plan'] == 1):
                price_id = settings.ENTERPRIZE_ADD_LIST
        else:
            if(data['plan'] == 1):
                price_id = settings.ECO_PRICE_ID
            if(data['plan'] == 2):
                price_id = settings.STANDARD_PRICE_ID
            if(data['plan'] == 3):
                price_id = settings.PRO_PRICE_ID
            if(data['plan'] == 1):
                price_id = settings.ENTERPISE_PRICE_ID       

        
        try:
            stripe.Subscription.modify(
                subscription.id,
                cancel_at_period_end=False,
                proration_behavior='create_prorations',
                items=[{
                    'id': subscription['items']['data'][0].id,
                    'price': price_id,
                }]
            )
            
            user.price_plan = data['plan']
            user.option_price = optprice_flag
            user.save()

            status_code = status.HTTP_200_OK 
            response = {
                'status': status_code,
                'type': 'successfully',
            } 

            return Response(response, status=status_code)
        except Exception as e: 
            return Response(status=status.HTTP_400_BAD_REQUEST)








class CreateCheckoutSessionView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):  
        user = request.user
        data = request.data        
        stripe.api_key = settings.STRIPE_SECRET_KEY

        customer = stripe.Customer.create(
                email = data['email']
            )
        user.customer_id = customer.id
        user.save()

        onetimepaymentIntents = stripe.PaymentIntent.create( 
            amount = 150000,
            currency = 'jpy',  
            payment_method_types = ['card'], 
        )    

        
        status_code = status.HTTP_200_OK
        response = {
            'success': 'True',   
            'data':onetimepaymentIntents.client_secret,
            'type': 'successfully',
        }
        return Response(response, status=status_code)







class GetPaymentStatus(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request): 
        user = request.user   

        three_dm_texts = DMtextSetModel.objects.all().order_by('-recent_send_date')[:3].values('pk', 'title10', 'sent_count', 'total_count')
        total_success_count = DMtextSetModel.objects.aggregate(total_success_count=Sum('sent_count'))
        total_sent_count = DMtextSetModel.objects.aggregate(total_sent_count=Sum('total_count'))

        print(total_sent_count)

        status_code = status.HTTP_200_OK
        response = {
            'success': 'True', 
            'status code': status_code,
            'paydate':user.paydate,
            'expirydate':user.expirydate,
            'account_statu':user.account_statu,
            'price_plan':user.price_plan,
            'payment_method':user.payment_method,
            'initial_pay_statu':user.initial_pay_statu,
            'three_dm_texts': three_dm_texts,
            'total_success_count':total_success_count,
            'total_sent_count':total_sent_count,
            'company':user.coporate_name,
            'company_type':user.company_type,
            'option_price':  user.option_price, 
            'username':str(user.firstname_of_charger) + " " + str(user.lastname_of_charger),
            'type': 'successfully',
        }

        return Response(response, status=status_code)





class SavePaymentMethod(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request): 
        user = request.user   
        data = request.data

        user.price_plan = data['paymethod']
        user.save()

        status_code = status.HTTP_200_OK
        response = {
            'success': 'True', 
            'status code': status_code, 
            'type': 'successfully',
        }
        return Response(response, status=status_code)




class SavePricePlan(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request): 
        user = request.user   
        data = request.data
        
        user.price_plan = data['plan']
        user.save()

        status_code = status.HTTP_200_OK
        response = {
            'success': 'True', 
            'status code': status_code, 
            'type': 'successfully',
        }
        return Response(response, status=status_code)




class GetBasicInfo(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request): 
        user = request.user    

        status_code = status.HTTP_200_OK
        response = {
            'success': 'True', 
            'coporate_name':  user.coporate_name,       
            'company_type':  user.company_type,         
            'corporate_furigana':  user.corporate_furigana,    
            'corporate_zipcode':  user.corporate_zipcode,        
            'corporate_country':  user.corporate_country,        
            'corporate_prefecture':  user.corporate_prefecture,        
            'corporate_city':  user.corporate_city,         
            'corporate_address':  user.corporate_address,         
            'corporate_building_name':  user.corporate_building_name,      
            'corporate_estable_date':  user.corporate_estable_date,         
            'corporate_phone':  user.corporate_phone,        
            'corporate_fax':  user.corporate_fax,        
            'corporate_mail':  user.corporate_mail,        
            'corporate_homepage':  user.corporate_homepage,       
            'corporate_address_room_number':  user.corporate_address_room_number,       
            'firstname_of_charger':  user.firstname_of_charger,          
            'lastname_of_charger':  user.lastname_of_charger,        
            'firstname_of_charger_firagana':  user.firstname_of_charger_firagana,     
            'lastname_of_charger_firagana':  user.lastname_of_charger_firagana,         
            'charger_prefecture':  user.charger_prefecture,          
            'choice_word':  user.choice_word,               
            'status code': status_code, 
            'type': 'successfully',
        }
        return Response(response, status=status_code)


class SetOptionPrice(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request): 
        user = request.user   
        data = request.data
        
        user.option_price = data['optionprice']
        user.save()

        status_code = status.HTTP_200_OK
        response = {
            'success': 'True', 
            'status code': status_code, 
            'type': 'successfully',
        }
        return Response(response, status=status_code)





class SetPaymentasBank(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request): 
        user = request.user 
        data = request.data   
 
        if data['isCheckOptionPrice']:
            user.option_price = 1
        else:
            user.option_price = 0
        user.price_plan = data['price_plan']
        user.payment_method = data['payment_method']
        user.save()
         
        status_code = status.HTTP_200_OK
        response = {
            'success': 'True', 
            'status code': status_code, 
            'type': 'successfully',
        }
        return Response(response, status=status_code)







# =================================================
# 
# ----------ADMIN SIDE-----------------------------
# 
# =================================================



 
class AdminLoginView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = AdminLoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data= request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            'status code' : status.HTTP_200_OK,
            'token' : serializer.data['token'],
            'refresh':serializer.data['refresh'],
            'userstatus':serializer.data['userstatus'],
            'email':serializer.data['email']
        }
        status_code = status.HTTP_200_OK
        return Response(response, status=status_code)

















#  NonCompleted===========================================================


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
            'type': 'successfully',
        }
        return Response(response, status=status_code)








#======================================== Function List==============================================


def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def send_mail_to(useremail, subject, message):
    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = [useremail]
    send_mail(subject, message, email_from, recipient_list)
    return True


def checkSendingCondition():  
    reserveTimer = th.Timer(180, checkSendingCondition)
    reserveTimer.start()

    if( is_time_between() and datetime.today().weekday() < 5):
        sendReservationDM()



def is_time_between(begin_time = time(9,00), end_time = time(23,00), check_time=None):    
    check_time = check_time or datetime.now().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time


def sendReservationDM(): 
    resdata = DMSendStatusModel.objects.filter(Q(status = "reservation"))
    if(resdata):
        for res_D in resdata:
            first_date = str(res_D.reserve_date)
            second_date = str(datetime.today())            
            user_mail_sess = SessionStore(session_key=Session_key) 
            main_data = eval(res_D.data) 
            tpattern = None            
            specific_day = res_D.specific_day
            reserve_date = res_D.reserve_date
            tpattern1_s = eval(res_D.textpattern1)
            tpattern2_s = eval(res_D.textpattern2)
            text_option_s = res_D.text_option

            if(first_date <= second_date and Session_key !=""):      
                user = User.objects.filter(Q(email = user_mail_sess['user_mail'])).first()  
                browser         = Browser()
                browser.set_handle_equiv(False)
                browser.set_handle_robots(False)
                browser.addheaders = [('User-agent','Mozilla/5.0 (X11; Linux x86_64; rv:18.0)Gecko/20100101 Firefox/18.0 (compatible;)'),('Accept', '*/*')]   
                
                global interupt_flag, total_result  
                                
                if(res_D.text_option == 1):
                    tpattern = eval(res_D.textpattern1)
                    reserveSendSubFunction(main_data, user, tpattern, browser, specific_day, reserve_date, tpattern1_s, tpattern2_s, text_option_s)
                if(res_D.text_option == 2):
                    tpattern = eval(res_D.textpattern2)
                    reserveSendSubFunction(main_data, user, tpattern, browser, specific_day, reserve_date, tpattern1_s, tpattern2_s, text_option_s)
                    tpattern = eval(res_D.textpattern1)
                    reserveSendSubFunction(main_data, user, tpattern, browser, specific_day, reserve_date, tpattern1_s, tpattern2_s, text_option_s)

 

def sendDMAutoMatic(data, user, tpattern):   
    global process_count, process_flag
    process_count   = 0
    process_flag    = False
    
    # createDriver()
 
    for d in data['rows']:
        try:
            t = th.Timer(0.001, process, [d, user, tpattern, len(data['rows'])])
            t.start()
        except Exception as e: 
            total_result.append({"status":"fail", "data": d }) 
         



def process(d, user, tpattern, all_count):    
    browser         = Browser()
    browser.set_handle_equiv(False)
    browser.set_handle_robots(False)
    browser.addheaders = [('User-agent','Mozilla/5.0 (X11; Linux x86_64; rv:18.0)Gecko/20100101 Firefox/18.0 (compatible;)'),('Accept', '*/*')]   
    
    global interupt_flag, total_result , process_count, process_flag, driver_lists
 

    if(interupt_flag == True):
        process_flag = True
        return
    else:
        URL = d['contact_url']                                
        ContactMail = d['mailaddress']    

        if(URL != ""):
            try:  
                page = requests.get(URL)
                soup = BeautifulSoup(page.content, "html.parser") 
                

                # Get Site Key
                sitekey = ""
                html        = str(soup)   

                if(html.count("'sitekey': '") > 0 \
                    or html.count("'sitekey':'") > 0 \
                        or html.count("'site-key': '") > 0 \
                            or html.count("'siteKey': '") > 0 \
                                or html.count("'site_key': '") > 0 ):

                    tags        = html.split("key': '")
                    tag         = tags[1]        
                    tags        = tag.split("'")
                    sitekey     = tags[0] 

                if(html.count("var sitekey = '") > 0):
                    tags        = html.split("var sitekey = '")
                    tag         = tags[1]        
                    tags        = tag.split("'")
                    sitekey     = tags[0] 

                if(html.count('data-sitekey="') > 0):
                    tags        = html.split('data-sitekey="')
                    tag         = tags[1]        
                    tags        = tag.split('"')
                    sitekey     = tags[0] 

                if(html.count('title="reCAPTCHA"') > 0):
                    tags        = html.split('k=')
                    tag         = tags[1]        
                    tags        = tag.split('&')
                    sitekey     = tags[0] 

                
                if(html.count('method="post"') < 1):
                    total_result.append({"status":"fail", "data": d }) 
                    process_count += 1
                    return 

                browser.open(URL) 
                browser.select_form(method='post')  

                browser.set_all_readonly(False) 
                browser.set_handle_equiv(True)
                browser.set_handle_redirect(True)
                browser.set_handle_referer(True)
                browser.set_handle_robots(False) 
                 
                print(sitekey)
                
                rd = "" 
                
                if(sitekey != ""):  
                    if rd == "":
                        solver = recaptchaV3Proxyless()
                        solver.set_verbose(1)
                        solver.set_key(ANTI_CAPTCHA_API_KEY)
                        solver.set_website_url(URL)
                        solver.set_website_key(sitekey)
                        solver.set_page_action("home_page")
                        solver.set_min_score(0.9) 

                        g_response = solver.solve_and_return_solution()
                        
                        if g_response != 0:
                            # print("g-response: "+g_response)
                            rd = str(g_response)
                        else:
                            print ("task finished with error "+solver.error_code) 

                    if rd == "":                    
                        solver = recaptchaV2Proxyless()
                        solver.set_verbose(1)
                        solver.set_key(ANTI_CAPTCHA_API_KEY)
                        solver.set_website_url(URL)
                        solver.set_website_key(sitekey)

                        g_response = solver.solve_and_return_solution()
                        if g_response != 0:
                            print("g-response: "+g_response)
                            rd = str(g_response)
                        else:
                            print ("task finished with error "+solver.error_code) 
                    
                    if rd == "":  
                        solver = hCaptchaProxyless()
                        solver.set_verbose(1)
                        solver.set_key(ANTI_CAPTCHA_API_KEY)
                        solver.set_website_url(URL)
                        solver.set_website_key(sitekey) 

                        g_response = solver.solve_and_return_solution()
                        if g_response != 0:
                            # print("g-response: "+g_response)
                            rd = str(g_response)
                        else:
                            print ("task finished with error "+solver.error_code) 

                form = soup.find('form')  

                NoneType = type(None)
                if isinstance(form, NoneType):
                    process_count += 1
                    return

                inputs = form.find_all('input') 
                textareas = form.find_all('textarea') 
                checkboxes = form.find_all(type = 'checkbox') 
                selects = form.select('select')    
                
                formTempData = {}    
                flag = False

                for input in inputs:   
                    if(interupt_flag == True):
                        break
                    else:
                        hasType = True
                        checkType = ""
                        try:
                            checkType = input['type']
                        except:
                            hasType = False
                        if hasType == True:  

                            if(input['type'] == "email"): 
                                key = input['name']
                                value = user.corporate_mail
                                formTempData[key] = value    

                            if(input['type'] == "url"): 
                                if str(user.corporate_homepage) != "null": 
                                    key = input['name']
                                    value = str(user.corporate_homepage)
                                    formTempData[key] = value   
                                else: 
                                    key = input['name']
                                    value = "https://test.com"
                                    formTempData[key] = value 

                            if(input['type'] == "date"): 
                                key = input['name']    
                                curtime = datetime.now()
                                value = str(datetime.strftime(curtime, '%Y-%m-%d'))
                                formTempData[key] = value  

                            if(input['type'] == "hidden"):
                                hasVal = True
                                checkVal = ""
                                try:
                                    checkVal = input['value']
                                except:
                                    hasVal = False
                                if hasVal:
                                    key = input['name']
                                    value = input['value']
                                    formTempData[key] = value                                                             

                            if(input['type'] == "text"): 
                                key = input['name']
                                value = "。"
                                formTempData[key] = value

                                if input['name'].find("city") != -1: 
                                    key = input['name']
                                    value = str(user.corporate_city)
                                    formTempData[key] = value
                                
                                if input['name'].find("text-809") != -1: 
                                    key = input['name']
                                    value = str(user.firstname_of_charger) + str(user.lastname_of_charger)
                                    formTempData[key] = value

                                if input['name'].find("chomei") != -1: 
                                    key = input['name']
                                    value = str(user.corporate_address)
                                    formTempData[key] = value

                                if input['name'].find("tatemono") != -1: 
                                    key = input['name']
                                    value = str(user.corporate_building_name)
                                    formTempData[key] = value

                                if input['name'].find("date") != -1:
                                    if input['name'].find("year") != -1: 
                                        key = input['name'] 
                                        curtime = datetime.now()
                                        value = str(datetime.strftime(curtime, '%Y'))
                                        formTempData[key] = value

                                    if input['name'].find("month") != -1: 
                                        key = input['name'] 
                                        curtime = datetime.now()
                                        value = str(datetime.strftime(curtime, '%m'))
                                        formTempData[key] = value

                                    if input['name'].find("day") != -1: 
                                        key = input['name'] 
                                        curtime = datetime.now()
                                        value = str(datetime.strftime(curtime, '%d'))
                                        formTempData[key] = value

                                    else: 
                                        key = input['name']
                                        curtime = datetime.now()
                                        value = str(datetime.strftime(curtime, '%Y-%m-%d'))
                                        formTempData[key] = value

                                if(input['name'].find("name") != -1 \
                                    or r"user_name" in input['name'] \
                                    or "_field_1_name" in input['name'] \
                                    or "tkna001" in input['name'] \
                                        or "_field_1_name_katakana" in input['name'] \
                                    or r"your-name" in input['name'] \
                                    or "contact_name" in input['name'] \
                                        or "名前" in input['name'] \
                                            or "f4a6f2b" in input['name'] \
                                                or "担当者" in input['name'] \
                                                    or "氏名" in input['name'] \
                                                        or "name" == input['name'] \
                                                            or "name1" == input['name'] \
                                                                or "text-978" == input['name'] \
                                                                    or "firstname" == input['name'] \
                                                                        or "full_name" == input['name'] \
                                                                            or "customer_name" == input['name'] \
                                                                                or "namae" in input['name'] \
                                                                                    or "form_fields[name]" in input['name']):  
                                    key = input['name']
                                    value = user.firstname_of_charger + user.lastname_of_charger
                                    formTempData[key] = value

                                if( "姓" == input['name'] \
                                    or "firstName" == input['name'] \
                                        or "first_name" == input['name'] \
                                            or "name1" == input['name'] \
                                            or "name-1" == input['name'] \
                                                or "FirstName" in input['name'] \
                                                    or "firstname" in input['name'] ):  
                                    key = input['name']
                                    value = user.firstname_of_charger
                                    formTempData[key] = value

                                if( "lastName" == input['name'] \
                                    or "name2" == input['name'] \
                                        or "名" == input['name'] \
                                            or "LastName" == input['name'] \
                                                or "name3" in input['name'] \
                                                or "name-2" in input['name'] \
                                                    or "lastname" in input['name'] ):  
                                    key = input['name']
                                    value = user.lastname_of_charger
                                    formTempData[key] = value

                                if(input['name'].find("comp") != -1 \
                                    or input['name'].find("cname") != -1 \
                                    or "organization" in input['name'] \
                                    or "your-company" in input['name'] \
                                    or "company-name" in input['name'] \
                                    or "_field_2" in input['name'] \
                                    or "kaisha-name" in input['name'] \
                                    or "company" == input['name'] \
                                    or "contact_company" == input['name'] \
                                    or "campany" in input['name'] \
                                    or "your-corp" in input['name'] \
                                    or "corporate" in input['name'] \
                                    or "企業" in input['name'] \
                                    or "社名" in input['name'] \
                                    or "text-978" == input['name'] \
                                    or "Company" in input['name'] \
                                    or "company3" == input['name'] \
                                    or "form_fields[company]" in input['name'] \
                                    or "text-819" == input['name']
                                ):  
                                    key = input['name']
                                    value = user.coporate_name
                                    formTempData[key] = value

                                if(input['name'].find("post") != -1 or input['name'].find("add") != -1 \
                                    or "your-post" in input['name'] \
                                        or "zip" in input['name'] \
                                            or "code" in input['name']): 
                                    key = input['name']
                                    value = user.corporate_zipcode
                                    formTempData[key] = value

                                if(input['name'].find("phon") != -1 \
                                    or "tel" in input['name'] \
                                        or input['name'].find("tel") != -1 \
                                            or input['name'].find("tkph") != -1 \
                                        or "TEL" in input['name'] \
                                            or "Tel" in input['name'] \
                                                or "電話" in input['name'] \
                                                    or "phone" in input['name'] \
                                                        or "Phone" in input['name']):   
                                    key = input['name']
                                    value = user.corporate_phone
                                    formTempData[key] = value

                                if(input['name'].find("fax") != -1): 
                                    key = input['name']
                                    value = user.corporate_fax
                                    formTempData[key] = value

                                if(input['name'].find("subject") != -1): 
                                    key = input['name']
                                    value = tpattern['title50']
                                    formTempData[key] = value
                                
                                if(input['name'].find("mail") != -1):  
                                    key = input['name']
                                    value = user.corporate_mail
                                    formTempData[key] = value 

                                if(input['name'].find("furigana") != -1 \
                                or "your-furiga" in input['name'] \
                                    or "userfuriga" in input['name'] \
                                        or "personal_furigana_name" in input['name'] \
                                            or "name_ruby" in input['name'] \
                                                or "ふりがな" in input['name'] ):  
                                    key = input['name']
                                    value = user.firstname_of_charger_firagana + user.lastname_of_charger_firagana
                                    formTempData[key] = value

                                if(input['name'].find("kana-1")) != -1: 
                                    key = input['name']
                                    value = user.firstname_of_charger_firagana 
                                    formTempData[key] = value

                                if input['name'] == "_field_3": 
                                    key = input['name']
                                    value = user.corporate_mail 
                                    formTempData[key] = value

                                if(input['name'].find("kana-2")) != -1: 
                                    key = input['name']
                                    value = user.lastname_of_charger_firagana 
                                    formTempData[key] = value
                                    

                                if(input['name'] == "quiz-31"): 
                                    browser[input['name']] = "東京"
                                    key = input['name']
                                    value = "東京"
                                    formTempData[key] = value
                                
                            if(input['type'] == "tel"):
                                if(input['name'].find("phon") != -1 \
                                    or "tel" in input['name'] \
                                        or "TEL" in input['name'] \
                                            or "Tel" in input['name'] \
                                                or "電話" in input['name'] \
                                                    or "phone" in input['name'] \
                                                        or "Phone" in input['name']):                             
                                    browser[input['name']] = user.corporate_phone
                                    key = input['name']
                                    value = user.corporate_phone
                                    formTempData[key] = value

                                if(input['name'].find("post") != -1 \
                                    or "your-post" in input['name'] \
                                        or "postalCode" in input['name'] \
                                            or "zip" in input['name']): 
                                    key = input['name']
                                    value = user.corporate_zipcode
                                    formTempData[key] = value
                            
                            if(input['type'] == "radio"):  
                                b_in_dict =  input['name'] in formTempData
                                if(b_in_dict != True): 
                                    key = input['name']
                                    value = [input['value']]
                                    formTempData[key] = value
                        
                         

                for textarea in textareas: 
                    if(interupt_flag == True):
                        break
                    else: 
                        maxLength = 0
                        try:
                            if str(textarea).find('maxlength="') !=-1: 
                                maxLength = str(textarea).split('maxlength="')[1]                                 
                                maxLength = str(maxLength).split('"')[0] 
                                maxLength = int(maxLength) 
                                
                                
                                if 0 < maxLength <= 100: 
                                    key = textarea['name']
                                    value = tpattern['text100']
                                    formTempData[key] = value 

                                if 100< maxLength < 251: 
                                    key = textarea['name']
                                    value = tpattern['text250']
                                    formTempData[key] = value

                                if 250 < maxLength < 501: 
                                    key = textarea['name']
                                    value = tpattern['text500']
                                    formTempData[key] = value

                                if 500 < maxLength < 1001: 
                                    key = textarea['name']
                                    value = tpattern['text1000']
                                    formTempData[key] = value
                                
                                else:
                                    key = textarea['name']
                                    value = tpattern['text100']
                                    formTempData[key] = value 

                        except:
                            maxLength = 0

                        if maxLength == 0:              
                            key = textarea['name']
                            value = tpattern['text100']
                            formTempData[key] = value 


                for select in selects: 
                    if(interupt_flag == True):
                        break
                    else:
                        if select['name'].find("state") != -1 \
                            or select['name'].find("pref") != -1:  
                            key = select['name'] 
                            value = str(user.corporate_prefecture)
                            formTempData[key] = value 

                        if select['name'].find("month") != -1: 
                            key = select['name']
                            value = datetime.now().month
                            formTempData[key] = value

                        if select['name'].find("year") != -1: 
                            key = select['name']
                            value = str(datetime.now().year)
                            formTempData[key] = value

                        if select['name'].find("day") != -1: 
                            key = select['name']
                            value = str(datetime.now().day)
                            formTempData[key] = value

                        else:
                            option = select.select('option')  
                            key = select['name'] 
                            value = option[2]['value']
                            formTempData[key] = value 

                for checkbox in checkboxes:  
                    if(interupt_flag == True):
                        break
                    else:
                        checkbox.selected =True
                        key = checkbox['name']
                        value = True
                        formTempData[key] = value 

                
                if(sitekey == ""): 
                    response = browser.submit()                    
                    cuurl = response.geturl()
                    urlArr = cuurl.split("/")

                    urlFirst = ''
                    i = 0
                    for u in urlArr:
                        if(i < len(urlArr) - 1):
                            urlFirst = urlFirst + u + "/"
                        i = i + 1
    
                    naction = form['action'] 
                    httpnaction = form['action'] 
                    
                    if(naction.find('./') != -1):
                        naction = naction.replace('./', "")   

                    if(naction.find('/') != -1):
                        naction = naction.replace('/', "")              
                    
                    comUrl = urlFirst + naction  

                    if httpnaction.find("http") != -1:
                        comUrl = httpnaction

                    if URL.find(httpnaction) != -1:
                        comUrl = URL
                    request_ans = requests.post(comUrl, data=formTempData)  
                    responsePageHTML = BeautifulSoup(request_ans.content, "html.parser") 

                    if str(responsePageHTML).find("入力内容に問題があります") != -1 \
                        or str(responsePageHTML).find("確認して再度お試し") != -1 \
                            or str(responsePageHTML).find("404 Not Found") != -1:
                        total_result.append({"status":"fail", "data": d }) 

                    else:
                        total_result.append({"status":"success", "data": d })    


                else:                     
                    if(rd == ""):
                        total_result.append({"status":"fail", "data": d }) 

                    else:
                        if(flag == False): 

                            urlArr = URL.split("/")
                            urlFirst = ''
                            i = 0
                            for u in urlArr:
                                if(i < len(urlArr) - 1):
                                    urlFirst = urlFirst + u + "/"
                                i = i + 1
                            
                            
                            if isinstance(form['action'], NoneType): 
                                return
                            naction = str(form['action'] )
                            httpnaction = str(form['action'] )
                            
                            if(naction.find('./') != -1):
                                naction = naction.replace('./', "")   

                            if(naction.find('/') != -1):
                                naction = naction.replace('/', "")              
                            
                            comUrl = urlFirst + naction  

                            if httpnaction.find("http") != -1:
                                comUrl = httpnaction
                            
                            if URL.find(httpnaction) != -1:
                                comUrl = URL

                            site_url = comUrl 
                            formTempData['g-recaptcha-response'] = rd 
                            request_ans = requests.post(site_url, data=formTempData)   
                            responsePageHTML = BeautifulSoup(request_ans.content, "html.parser") 

                            if str(responsePageHTML).find("入力内容に問題があります") != -1 \
                                or str(responsePageHTML).find("確認して再度お試し") != -1 \
                                    or str(responsePageHTML).find("404 Not Found") != -1:
                                total_result.append({"status":"fail", "data": d }) 

                            else:
                                total_result.append({"status":"success", "data": d })
                                 
            except Exception as e: 
                print(e)
                traceback.print_exc()
                total_result.append({"status":"fail", "data": d })


        if(ContactMail != "" and URL == ""):   
            try:             
                total_result.append({"status":"mail", "data": d })
                
                from_email = settings.DEFAULT_FROM_EMAIL
                to=[user.email]
                subject = "お問い合わせメッセージが届きました。"
                message = "お問い合わせメッセージが届きました。"
                html = '\
                <h4>タイトル</h4><br/>\
                '+ tpattern['title50'] +'<br/>\
                <h4>内容</h4><br/>\
                ーーーーーーーーーーーーーーーーーーーーーーーーーーー<br/>\
                <br/>\
                ' + tpattern['text1000'] + '<br/>'

                send_mail(subject, message, from_email, to, html_message=html)

            except Exception as e: 
                total_result.append({"status":"fail", "data": d })


        if(ContactMail == "" and URL == ""):                
            total_result.append({"status":"fail", "data": d })

    
    process_count += 1
    
    if process_count == all_count:
        process_flag = True      














def reserveSendSubFunction(main_data, user, tpattern, browser, specific_day, reserve_date, tpattern1_s, tpattern2_s, text_option_s):
    URL = main_data['contact_url']                                
    ContactMail = main_data['mailaddress']                                
    subtotal_result = [] 
     
    if(URL != ""):
        try:
            page = requests.get(URL)  
            soup = BeautifulSoup(page.content, "html.parser")  

            # Get Site Key
            sitekey = ""
            html        = str(soup) 
            
            if(html.count("'sitekey': '") > 0 \
                or html.count("'sitekey':'") > 0 \
                    or html.count("'site-key': '") > 0 \
                        or html.count("'siteKey': '") > 0 \
                            or html.count("'site_key': '") > 0 ):

                tags        = html.split("key': '")
                tag         = tags[1]        
                tags        = tag.split("'")
                sitekey     = tags[0] 

            if(html.count("var sitekey = '") > 0):
                tags        = html.split("var sitekey = '")
                tag         = tags[1]        
                tags        = tag.split("'")
                sitekey     = tags[0] 

            if(html.count('data-sitekey="') > 0):
                tags        = html.split('data-sitekey="')
                tag         = tags[1]        
                tags        = tag.split('"')
                sitekey     = tags[0] 

            if(html.count('title="reCAPTCHA"') > 0):
                tags        = html.split('k=')
                tag         = tags[1]        
                tags        = tag.split('&')
                sitekey     = tags[0] 

            
            if(html.count('method="post"') < 1):
                subtotal_result.append({"status":"fail", "data": main_data }) 
                

            browser.open(URL) 
            browser.select_form(method='post')  

            browser.set_all_readonly(False) 
            browser.set_handle_equiv(True)
            browser.set_handle_redirect(True)
            browser.set_handle_referer(True)
            browser.set_handle_robots(False) 

            # reCaptcha sector
            rd = ""

            if(sitekey != ""):
                if rd == "":
                    solver = recaptchaV3Proxyless()
                    solver.set_verbose(1)
                    solver.set_key(ANTI_CAPTCHA_API_KEY)
                    solver.set_website_url(URL)
                    solver.set_website_key(sitekey)
                    solver.set_page_action("home_page")
                    solver.set_min_score(0.9) 

                    g_response = solver.solve_and_return_solution()
                    
                    if g_response != 0:
                        # print("g-response: "+g_response)
                        rd = str(g_response)
                    else:
                        print ("task finished with error "+solver.error_code) 

                if rd == "":                    
                    solver = recaptchaV2Proxyless()
                    solver.set_verbose(1)
                    solver.set_key(ANTI_CAPTCHA_API_KEY)
                    solver.set_website_url(URL)
                    solver.set_website_key(sitekey)

                    g_response = solver.solve_and_return_solution()
                    if g_response != 0:
                        print("g-response: "+g_response)
                        rd = str(g_response)
                    else:
                        print ("task finished with error "+solver.error_code) 
                
                if rd == "":  
                    solver = hCaptchaProxyless()
                    solver.set_verbose(1)
                    solver.set_key(ANTI_CAPTCHA_API_KEY)
                    solver.set_website_url(URL)
                    solver.set_website_key(sitekey) 

                    g_response = solver.solve_and_return_solution()
                    if g_response != 0:
                        # print("g-response: "+g_response)
                        rd = str(g_response)
                    else:
                        print ("task finished with error "+solver.error_code) 


            #End Get Site Key

            form = soup.find('form')  
            inputs = form.find_all('input') 
            textareas = form.find_all('textarea') 
            checkboxes = form.find_all(type = 'checkbox') 
            selects = form.select('select')    
            
            formTempData = {}    
            flag = False
                
            for input in inputs:  
                hasType = True
                checkType = ""
                try:
                    checkType = input['type']
                except:
                    hasType = False
                if hasType == True:  
                    if(input['type'] == "email"):
                        browser[input['name']] = user.corporate_mail
                        key = input['name']
                        value = user.corporate_mail
                        formTempData[key] = value       

                    if(input['type'] == "url"):
                        if str(user.corporate_homepage) != "null": 
                            key = input['name']
                            value = str(user.corporate_homepage)
                            formTempData[key] = value   
                        else: 
                            key = input['name']
                            value = "https://test.com"
                            formTempData[key] = value  

                    if(input['type'] == "hidden"):
                        hasVal = True
                        checkVal = ""
                        try:
                            checkVal = input['value']
                        except:
                            hasVal = False
                        if hasVal:
                            browser[input['name']] = input['value']
                            key = input['name']
                            value = input['value']
                            formTempData[key] = value     

                    if(input['type'] == "date"):
                        curtime = datetime.now()
                        value = str(datetime.strftime(curtime, '%Y-%m-%d'))
                        browser[input['name']] = value
                        key = input['name'] 
                        formTempData[key] = value                                 

                    if(input['type'] == "text"):
                        browser[input['name']] = '。'
                        key = input['name']
                        value = "。"
                        formTempData[key] = value

                        if input['name'].find("city") != -1:
                            browser[input['name']] = str(user.corporate_city)
                            key = input['name']
                            value = str(user.corporate_city)
                            formTempData[key] = value

                        if input['name'].find("chomei") != -1:
                            browser[input['name']] = str(user.corporate_address)
                            key = input['name']
                            value = str(user.corporate_address)
                            formTempData[key] = value
                        
                        if input['name'].find("tatemono") != -1:
                            browser[input['name']] = str(user.corporate_building_name)
                            key = input['name']
                            value = str(user.corporate_building_name)
                            formTempData[key] = value

                        if input['name'].find("date") != -1:
                            if input['name'].find("year") != -1: 
                                key = input['name'] 
                                curtime = datetime.now()
                                value = str(datetime.strftime(curtime, '%Y'))
                                formTempData[key] = value

                            if input['name'].find("month") != -1: 
                                key = input['name'] 
                                curtime = datetime.now()
                                value = str(datetime.strftime(curtime, '%m'))
                                formTempData[key] = value

                            if input['name'].find("day") != -1: 
                                key = input['name'] 
                                curtime = datetime.now()
                                value = str(datetime.strftime(curtime, '%d'))
                                formTempData[key] = value

                            else: 
                                key = input['name']
                                curtime = datetime.now()
                                value = str(datetime.strftime(curtime, '%Y-%m-%d'))
                                formTempData[key] = value

                        if(input['name'].find("name") != -1 \
                            or r"user_name" in input['name'] \
                            or "_field_1_name" in input['name'] \
                            or "tkna001" in input['name'] \
                                or "_field_1_name_katakana" in input['name'] \
                            or r"your-name" in input['name'] \
                            or "contact_name" in input['name'] \
                                or "名前" in input['name'] \
                                    or "f4a6f2b" in input['name'] \
                                        or "担当者" in input['name'] \
                                            or "氏名" in input['name'] \
                                                or "name" == input['name'] \
                                                    or "name1" == input['name'] \
                                                        or "text-978" == input['name'] \
                                                            or "firstname" == input['name'] \
                                                                or "full_name" == input['name'] \
                                                                    or "customer_name" == input['name'] \
                                                                        or "namae" in input['name'] \
                                                                            or "form_fields[name]" in input['name']): 
                            browser[input['name']] = user.firstname_of_charger + user.lastname_of_charger
                            key = input['name']
                            value = user.firstname_of_charger + user.lastname_of_charger
                            formTempData[key] = value

                        if( "姓" == input['name'] \
                            or "firstName" == input['name'] \
                                or "first_name" == input['name'] \
                                    or "name1" == input['name'] \
                                    or "name-1" == input['name'] \
                                        or "FirstName" in input['name'] \
                                            or "firstname" in input['name'] ): 
                            browser[input['name']] = user.firstname_of_charger 
                            key = input['name']
                            value = user.firstname_of_charger
                            formTempData[key] = value

                        if( "lastName" == input['name'] \
                            or "name2" == input['name'] \
                                or "名" == input['name'] \
                                    or "LastName" == input['name'] \
                                        or "name3" in input['name'] \
                                        or "name-2" in input['name'] \
                                            or "lastname" in input['name'] ): 
                            browser[input['name']] = user.lastname_of_charger 
                            key = input['name']
                            value = user.lastname_of_charger
                            formTempData[key] = value

                        if(input['name'].find("comp") != -1 \
                            or input['name'].find("cname") != -1 \
                            or "organization" in input['name'] \
                            or "your-company" in input['name'] \
                            or "company-name" in input['name'] \
                            or "_field_2" in input['name'] \
                            or "kaisha-name" in input['name'] \
                            or "company" == input['name'] \
                            or "contact_company" == input['name'] \
                            or "campany" in input['name'] \
                            or "your-corp" in input['name'] \
                            or "corporate" in input['name'] \
                            or "企業" in input['name'] \
                            or "社名" in input['name'] \
                            or "text-978" == input['name'] \
                            or "Company" in input['name'] \
                            or "company3" == input['name'] \
                            or "form_fields[company]" in input['name'] \
                            or "text-819" == input['name']
                        ): 
                            browser[input['name']] = user.coporate_name
                            key = input['name']
                            value = user.coporate_name
                            formTempData[key] = value

                        if(input['name'].find("post") != -1 or input['name'].find("add") != -1 \
                            or "your-post" in input['name'] \
                                or "zip" in input['name'] \
                                    or "code" in input['name']):
                            browser[input['name']] = user.corporate_zipcode
                            key = input['name']
                            value = user.corporate_zipcode
                            formTempData[key] = value

                        if(input['name'].find("phon") != -1 \
                            or "tel" in input['name'] \
                            or input['name'].find("tkph") != -1 \
                                or input['name'].find("tel") != -1 \
                                or "TEL" in input['name'] \
                                    or "Tel" in input['name'] \
                                        or "電話" in input['name'] \
                                            or "phone" in input['name'] \
                                                or "Phone" in input['name']):  
                            browser[input['name']] = user.corporate_phone
                            key = input['name']
                            value = user.corporate_phone
                            formTempData[key] = value

                        if(input['name'].find("fax") != -1):
                            browser[input['name']] = user.corporate_fax
                            key = input['name']
                            value = user.corporate_fax
                            formTempData[key] = value

                        if(input['name'].find("subject") != -1):
                            browser[input['name']] = tpattern['title50']
                            key = input['name']
                            value = tpattern['title50']
                            formTempData[key] = value
                        
                        if(input['name'].find("mail") != -1): 
                            browser[input['name']] = user.corporate_mail
                            key = input['name']
                            value = user.corporate_mail
                            formTempData[key] = value

                        if(input['name'].find("furigana") != -1 \
                        or "your-furiga" in input['name'] \
                            or "userfuriga" in input['name'] \
                                or "personal_furigana_name" in input['name'] \
                                    or "name_ruby" in input['name'] \
                                        or "ふりがな" in input['name'] ): 
                            browser[input['name']] = user.firstname_of_charger_firagana + user.lastname_of_charger_firagana
                            key = input['name']
                            value = user.firstname_of_charger_firagana + user.lastname_of_charger_firagana
                            formTempData[key] = value

                        if(input['name'].find("kana-1")) != -1:
                            browser[input['name']] = user.firstname_of_charger_firagana 
                            key = input['name']
                            value = user.firstname_of_charger_firagana 
                            formTempData[key] = value

                        if(input['name'].find("kana-2")) != -1:
                            browser[input['name']] = user.lastname_of_charger_firagana 
                            key = input['name']
                            value = user.lastname_of_charger_firagana 
                            formTempData[key] = value
                        
                        if input['name'] == "_field_3":
                            browser[input['name']] = user.corporate_mail 
                            key = input['name']
                            value = user.corporate_mail 
                            formTempData[key] = value
                            

                        if(input['name'] == "quiz-31"): 
                            browser[input['name']] = "東京"
                            key = input['name']
                            value = "東京"
                            formTempData[key] = value
                        
                    if(input['type'] == "tel"):
                        if(input['name'].find("phon") != -1 \
                            or "tel" in input['name'] \
                                or "TEL" in input['name'] \
                                    or "Tel" in input['name'] \
                                        or "電話" in input['name'] \
                                            or "phone" in input['name'] \
                                                or "Phone" in input['name']):                             
                            browser[input['name']] = user.corporate_phone
                            key = input['name']
                            value = user.corporate_phone
                            formTempData[key] = value

                        if(input['name'].find("post") != -1 \
                            or "your-post" in input['name'] \
                                or "postalCode" in input['name'] \
                                    or "zip" in input['name']):
                            browser[input['name']] = user.corporate_zipcode
                            key = input['name']
                            value = user.corporate_zipcode
                            formTempData[key] = value
                    
                    if(input['type'] == "radio"):  
                        b_in_dict =  input['name'] in formTempData
                        if(b_in_dict != True):
                            browser[input['name']] = [input['value']]
                            key = input['name']
                            value = [input['value']]
                            formTempData[key] = value
                
                 
            for textarea in textareas: 
                maxLength = 0
                try:
                    if str(textarea).find('maxlength="') !=-1:
                        maxLength = str(textarea).split('maxlength="')[1]
                        maxLength = str(maxLength).split('"')[0]
                        maxLength = int(maxLength)                         

                        if 0 < maxLength <= 100: 
                            key = textarea['name']
                            value = tpattern['text100']
                            formTempData[key] = value 

                        if 100< maxLength < 251: 
                            key = textarea['name']
                            value = tpattern['text250']
                            formTempData[key] = value

                        if 250 < maxLength < 501: 
                            key = textarea['name']
                            value = tpattern['text500']
                            formTempData[key] = value

                        if 500 < maxLength < 1001: 
                            key = textarea['name']
                            value = tpattern['text1000']
                            formTempData[key] = value
                        
                        else:
                            key = textarea['name']
                            value = tpattern['text100']
                            formTempData[key] = value 

                except:
                    maxLength = 0

                if maxLength == 0:              
                    key = textarea['name']
                    value = tpattern['text1000']
                    formTempData[key] = value


            for select in selects:                 
                if select['name'].find("state") != -1 \
                    or select['name'].find("pref") != -1: 
                    browser[select['name']] = str(user.corporate_prefecture)
                    key = select['name'] 
                    value = str(user.corporate_prefecture)
                    formTempData[key] = value 

                if select['name'].find("month") != -1:
                    browser[select['name']] = str(datetime.now().month)
                    key = select['name']
                    value = str(datetime.now().month)
                    formTempData[key] = value

                if select['name'].find("year") != -1:
                    browser[select['name']] = str(datetime.now().year)
                    key = select['name']
                    value = str(datetime.now().year)
                    formTempData[key] = value

                if select['name'].find("day") != -1:
                    browser[select['name']] = str(datetime.now().day)
                    key = select['name']
                    value = str(datetime.now().day)
                    formTempData[key] = value

                else:
                    option = select.select('option') 
                    browser[select['name']] = [option[2]['value']]
                    key = select['name'] 
                    value = option[2]['value']
                    formTempData[key] = value  

            for checkbox in checkboxes:                  
                checkbox.selected =True
                key = checkbox['name']
                value = True
                formTempData[key] = value 

            
            if(sitekey == ""):
                response = browser.submit()
                cuurl = response.geturl()
                urlArr = cuurl.split("/")

                urlFirst = ''
                i = 0
                for u in urlArr:
                    if(i < len(urlArr) - 1):
                        urlFirst = urlFirst + u + "/"
                    i = i + 1

                naction = form['action'] 
                httpnaction = form['action'] 
                
                if(naction.find('./') != -1):
                    naction = naction.replace('./', "")   

                if(naction.find('/') != -1):
                    naction = naction.replace('/', "")              
                
                comUrl = urlFirst + naction  

                if httpnaction.find("http") != -1:
                    comUrl = httpnaction

                if URL.find(httpnaction) != -1:
                    comUrl = URL     

                request_ans = requests.post(comUrl, data=formTempData)  
                responsePageHTML = BeautifulSoup(request_ans.content, "html.parser") 

                if str(responsePageHTML).find("入力内容に問題があります") != -1 \
                    or str(responsePageHTML).find("確認して再度お試し") != -1 \
                        or str(responsePageHTML).find("404 Not Found") != -1:
                    total_result.append({"status":"fail", "data": main_data }) 

                else:
                    subtotal_result.append({"status":"success", "data": main_data })   

                    
            else:                 
                if(rd == ""):
                    subtotal_result.append({"status":"fail", "data": main_data }) 

                else:
                    if(flag == False): 

                        urlArr = URL.split("/")
                        urlFirst = ''
                        i = 0
                        for u in urlArr:
                            if(i < len(urlArr) - 1):
                                urlFirst = urlFirst + u + "/"
                            i = i + 1
                        
                        
                        if isinstance(form['action'], NoneType): 
                            return
                        naction = str(form['action'] )
                        httpnaction = str(form['action'] )
                        
                        if(naction.find('./') != -1):
                            naction = naction.replace('./', "")   

                        if(naction.find('/') != -1):
                            naction = naction.replace('/', "")              
                        
                        comUrl = urlFirst + naction  

                        if httpnaction.find("http") != -1:
                            comUrl = httpnaction

                        if URL.find(httpnaction) != -1:
                                comUrl = URL

                        site_url = comUrl
 
                        formTempData['g-recaptcha-response'] = rd 

                        request_ans = requests.post(site_url, data=formTempData) 
                        ans_html = BeautifulSoup(request_ans.content, "html.parser") 
                        if str(ans_html).find("入力内容に問題があります") != -1 \
                                or str(responsePageHTML).find("確認して再度お試し") != -1 \
                                    or str(responsePageHTML).find("404 Not Found") != -1:

                            subtotal_result.append({"status":"fail", "data": main_data })

                        else:
                            subtotal_result.append({"status":"success", "data": main_data })                     

        except Exception as e: 
            subtotal_result.append({"status":"success", "data": main_data })
    
    if(ContactMail != "" and URL == ""):   
        try:
            subtotal_result.append({"status":"mail", "data": main_data })                
            from_email = settings.DEFAULT_FROM_EMAIL
            to=[user.email]
            subject = "お問い合わせメッセージが届きました。"
            message = "お問い合わせメッセージが届きました。"
            html = '\
            <h4>タイトル</h4><br/>\
            '+ tpattern['title50'] +'<br/>\
            <h4>内容</h4><br/>\
            ーーーーーーーーーーーーーーーーーーーーーーーーーーー<br/>\
            <br/>\
            ' + tpattern['text1000'] + '<br/>'

            send_mail(subject, message, from_email, to, html_message=html)

        except Exception as e: 
            subtotal_result.append({"status":"success", "data": main_data })

    if(ContactMail == "" and URL == ""):      
        subtotal_result.append({"status":"fail", "data": main_data })   

 

    for req_data_item in subtotal_result: 
        
        resdata = PerDMGroupDmListModel.objects.filter(Q(id = req_data_item['data']['tb_id'])).first()
        resdata.last_sent_date = datetime.now()
        resdata.last_sent_user = user.firstname_of_charger + user.lastname_of_charger
        resdata.save()

        totalsendcount = user.total_send_count + len(subtotal_result)
        user.total_send_count  = totalsendcount

        if(req_data_item['status'] == "fail"):
            user.total_send_faild_count = user.total_send_faild_count + 1

        if(req_data_item['status'] == "success"):
            user.total_send_success_count = user.total_send_success_count + 1

        if(req_data_item['status'] == "mail"):
            user.total_mail_send_count = user.total_mail_send_count + 1

        user.save()

        
        dmtexttable = DMtextSetModel.objects.filter(Q(id = tpattern['pk'])).first()
        if dmtexttable:
            dmtexttable.total_count = dmtexttable.total_count + 1
            if(req_data_item['status'] == "success" or req_data_item['status'] == "mail"):
                dmtexttable.sent_count = dmtexttable.sent_count + 1
        dmtexttable.save()
        
        DMSendStatusModel.objects.create(
            data            = req_data_item['data'], 
            status          = req_data_item['status'],
            list_table_id   = req_data_item['data']['tb_id'],
            reserve_date    = reserve_date,
            specific_day    = specific_day,
            textpattern1    = tpattern1_s,
            textpattern2    = tpattern2_s,
            text_option     = text_option_s,
            user            = user       
        )

    dmtexttable = DMtextSetModel.objects.filter(Q(id = tpattern['pk'])).first()
    if dmtexttable:
        dmtexttable.recent_send_date = datetime.now() 
        dmtexttable.save()





def sendManuallySubFunction(data, user, tpattern): 
    for d in data['rows']:
        URL = d['contact_url']                                
        ContactMail = d['mailaddress']

        global html_str, html_strs, all_form_datas, form_datas, site_urls, site_url

        try:
            if(URL != ""):               
                page = requests.get(URL)
                soup = BeautifulSoup(page.content, "html.parser") 
                
                html_str = str(soup)            

                form = soup.find('form') 
                  
                if isinstance(form, NoneType):
                    continue

                urlArr = URL.split("/")

                urlFirst = ''
                i = 0
                for u in urlArr:
                    if(i < len(urlArr) - 1):
                        urlFirst = urlFirst + u + "/"
                    i = i + 1
                
                
                if isinstance(form['action'], NoneType): 
                    continue
                naction = str(form['action'] )
                httpnaction = str(form['action'])
                
                if(naction.find('./') != -1):
                    naction = naction.replace('./', "")   

                if(naction.find('/') != -1):
                    naction = naction.replace('/', "")              
                
                comUrl = urlFirst + naction  

                if httpnaction.find("http") != -1:
                    comUrl = httpnaction

                site_url = comUrl
    

                inputs = form.find_all('input') 
                textareas = form.find_all('textarea') 
                checkboxes = form.find_all(type = 'checkbox') 
                selects = form.select('select')                    
                 
                
                for input in inputs:  
                    hasType = True
                    checkType = ""
                    try:
                        checkType = input['type']
                    except:
                        hasType = False
                    if hasType == True: 
                        if(input['name'].find("_field_3_confirm")) != -1:
                                form_datas.append({"tag":"input", "name":input['name'], "value":str(user.corporate_mail)})

                        if(input['type'] == "email"):                                                               
                            form_datas.append({"tag":"input", "name":input['name'], "value":str(user.corporate_mail)})
                            print("HERE============", input['type'])
                        
                        if(input['type'] == "text"):
                            if input['name'].find("city") != -1:
                                print("HERE========city====")
                                form_datas.append({"tag":"input", "name":input['name'], "value":str(user.corporate_city)})
                            
                            if input['name'].find("chomei") != -1:
                                print("HERE========chomei====")
                                form_datas.append({"tag":"input", "name":input['name'], "value":str(user.corporate_address)})

                            if input['name'].find("tatemono") != -1:
                                print("HERE========tatemono====")
                                form_datas.append({"tag":"input", "name":input['name'], "value":str(user.corporate_building_name)})

                            if input['name'].find("date") != -1:     
                                curtime = datetime.now()                            
                                if input['name'].find("year") != -1:
                                    form_datas.append({"tag":"input", "name":input['name'], "value":str(datetime.strftime(curtime, '%Y'))})                                    

                                if input['name'].find("month") != -1:
                                    form_datas.append({"tag":"input", "name":input['name'], "value":str(datetime.strftime(curtime, '%m'))})                                     

                                if input['name'].find("day") != -1:
                                    form_datas.append({"tag":"input", "name":input['name'], "value":str(datetime.strftime(curtime, '%d'))})   

                                else:
                                    form_datas.append({"tag":"input", "name":input['name'], "value":str(datetime.strftime(curtime, '%Y-%m-%d'))})  


                            if(input['name'].find("name") != -1 \
                                or r"user_name" in input['name'] \
                                or r"your-name" in input['name'] \
                                    or "_field_1_name" in input['name'] \
                                    or "tkna001" in input['name'] \
                                        or "_field_1_name_katakana" in input['name'] \
                                or "contact_name" in input['name'] \
                                    or "名前" in input['name'] \
                                        or "f4a6f2b" in input['name'] \
                                            or "担当者" in input['name'] \
                                                or "氏名" in input['name'] \
                                                    or "name" == input['name'] \
                                                        or "name1" == input['name'] \
                                                            or "text-978" == input['name'] \
                                                                or "firstname" == input['name'] \
                                                                    or "full_name" == input['name'] \
                                                                        or "customer_name" == input['name'] \
                                                                            or "namae" in input['name'] \
                                                                                or "form_fields[name]" in input['name']):                         
                                
                                form_datas.append({"tag":"input", "name":input['name'], "value":str(user.firstname_of_charger) + str(user.lastname_of_charger)})
                            
                            if( "姓" == input['name'] \
                                or "firstName" == input['name'] \
                                    or "first_name" == input['name'] \
                                        or "name1" == input['name'] \
                                        or "name-1" == input['name'] \
                                            or "FirstName" in input['name'] \
                                                or "firstname" in input['name'] ):  
                                form_datas.append({"tag":"input", "name":input['name'], "value":str(user.firstname_of_charger)})                        
                                 
                            if( "lastName" == input['name'] \
                                or "name2" == input['name'] \
                                    or "名" == input['name'] \
                                        or "LastName" == input['name'] \
                                            or "name3" in input['name'] \
                                            or "name-2" in input['name'] \
                                                or "lastname" in input['name'] ): 
                                
                                form_datas.append({"tag":"input", "name":input['name'], "value":str(user.lastname_of_charger)})   
                                   
                            if(input['name'].find("comp") != -1 \
                                or input['name'].find("cname") != -1 \
                                or "organization" in input['name'] \
                                or "your-company" in input['name'] \
                                or "company-name" in input['name'] \
                                or "_field_2" in input['name'] \
                                or "kaisha-name" in input['name'] \
                                or "company" == input['name'] \
                                or "contact_company" == input['name'] \
                                or "campany" in input['name'] \
                                or "your-corp" in input['name'] \
                                or "corporate" in input['name'] \
                                or "企業" in input['name'] \
                                or "社名" in input['name'] \
                                or "text-978" == input['name'] \
                                or "Company" in input['name'] \
                                or "company3" == input['name'] \
                                or "form_fields[company]" in input['name'] \
                                or "text-819" == input['name']
                            ): 
                                
                                form_datas.append({"tag":"input", "name":input['name'], "value":str(user.coporate_name)})                                                 
                                
                            if(input['name'].find("post") != -1 or input['name'].find("add") != -1 \
                                or "your-post" in input['name'] \
                                    or "zip" in input['name'] \
                                        or "code" in input['name']):

                                form_datas.append({"tag":"input", "name":input['name'], "value":str(user.corporate_zipcode)})   
                                
                            if(input['name'].find("phon") != -1 \
                                or "tel" in input['name'] \
                                    or "TEL" in input['name'] \
                                        or input['name'].find("tkph") != -1 \
                                        or input['name'].find("tel") != -1 \
                                        or "Tel" in input['name'] \
                                            or "電話" in input['name'] \
                                                or "phone" in input['name'] \
                                                    or "Phone" in input['name']):  

                                form_datas.append({"tag":"input", "name":input['name'], "value":str(user.corporate_phone)}) 
                                
                            if(input['name'].find("fax") != -1):
                                form_datas.append({"tag":"input", "name":input['name'], "value":str(user.corporate_fax)})       
                                
                            if(input['name'].find("subject") != -1):
                                form_datas.append({"tag":"input", "name":input['name'], "value":tpattern['title50']})          
                                
                            if(input['name'].find("mail") != -1): 
                                form_datas.append({"tag":"input", "name":input['name'], "value":str(user.corporate_mail)})  
                                
                            if(input['name'].find("furigana") != -1 \
                                or "your-furiga" in input['name'] \
                                    or "userfuriga" in input['name'] \
                                        or "personal_furigana_name" in input['name'] \
                                            or "name_ruby" in input['name'] \
                                                or "ふりがな" in input['name'] ): 
                                
                                form_datas.append({"tag":"input", "name":input['name'], "value":str(user.firstname_of_charger_firagana) + str(user.lastname_of_charger_firagana)})  

                            if(input['name'].find("kana-1")) != -1:
                                form_datas.append({"tag":"input", "name":input['name'], "value":str(user.firstname_of_charger_firagana)})                              

                            if input['name'] == "_field_3":
                                form_datas.append({"tag":"input", "name":input['name'], "value":str(user.corporate_mail)})                              
                            
                            if(input['name'].find("_field_3_confirm")) != -1:
                                form_datas.append({"tag":"input", "name":input['name'], "value":str(user.corporate_mail)})                              

                            if(input['name'].find("kana-2")) != -1:
                                form_datas.append({"tag":"input", "name":input['name'], "value":str(user.lastname_of_charger_firagana)}) 
                                
                            if(input['name'] == "quiz-31"): 
                                form_datas.append({"tag":"input", "name":input['name'], "value":"東京"}) 

                        if input['type'] == "tel":
                            if(input['name'].find("phon") != -1 \
                                or "tel" in input['name'] \
                                    or "TEL" in input['name'] \
                                        or "Tel" in input['name'] \
                                            or "電話" in input['name'] \
                                                or "phone" in input['name'] \
                                                    or "Phone" in input['name']):   
                                form_datas.append({"tag":"input", "name":input['name'], "value":str(user.corporate_phone)})
                                

                            if(input['name'].find("post") != -1 \
                                or "your-post" in input['name'] \
                                    or "postalCode" in input['name'] \
                                        or "zip" in input['name']):

                                form_datas.append({"tag":"input", "name":input['name'], "value":str(user.corporate_zipcode)}) 
                                

                        if(input['type'] == "radio"):  
                            form_datas.append({"tag":"input", "name":input['name'], "value":input['value']})

                        if(input['type'] == "hidden"):  
                            hasVal = True
                            checkVal = ""
                            try:
                                checkVal = input['value']
                            except:
                                hasVal = False
                            if hasVal:
                                form_datas.append({"tag":"input", "name":input['name'], "value":input['value']})
                    else:
                        if(input['name'].find("_field_3_confirm")) != -1:
                            form_datas.append({"tag":"input", "name":input['name'], "value":str(user.corporate_mail)})         
                
                for textarea in textareas:  
                    form_datas.append({"tag":"textarea", "name":textarea['name'], "value":tpattern['text1000']})   

                for select in selects: 
                    if select['name'].find("state") != -1 \
                        or select['name'].find("pref") != -1: 
                        form_datas.append({"tag":"select", "name":select['name'], "value":str(user.corporate_prefecture)})     
                    
                    if select['name'].find("month") != -1:
                        form_datas.append({"tag":"select", "name":select['name'], "value":str(datetime.now().month)})

                    if select['name'].find("year") != -1:
                        form_datas.append({"tag":"select", "name":select['name'], "value":str(datetime.now().year)})
                         
                    if select['name'].find("day") != -1:
                        form_datas.append({"tag":"select", "name":select['name'], "value":str(datetime.now().day)})
                         
                    else:
                        option = select.select('option') 
                        form_datas.append({"tag":"select", "name":select['name'], "value":option[2]['value']})         

                for checkbox in checkboxes:   
                    form_datas.append({"tag":"checkbox", "name":checkbox['name'], "value":"checkbox"})      

                html_strs.append({"page_html": html_str})            
                all_form_datas.append({"page_form_data": form_datas})
                site_urls.append({"page_site_url": site_url})                

                html_str = ""
                form_datas = []
                site_url = ""

        except Exception as e:  
            html_strs.append({"page_html": ""})            
            all_form_datas.append({"page_form_data": []})
            site_urls.append({"page_site_url": ""})             

