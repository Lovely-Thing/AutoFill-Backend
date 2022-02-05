# from crypt import methods
from cgi import print_directory
import email
from optparse import Option
from pickle import FALSE, NONE
from select import select
from sys import flags
from traceback import print_tb
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
from datetime import date, datetime, time
import threading as th  
from django.contrib.sessions.backends.db import SessionStore 
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from django.db.models import Sum


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
            'type': 'User registered  successfully',
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
            'type': 'User registered  successfully',
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
                'type': 'User registered  successfully',
            }
            return Response(response, status=status_code)

        else: 
            status_code = status.HTTP_200_OK
            response = {
                'success': 'True',
                'method': 1,
                'corporate_homepage':user.corporate_homepage,
                'status code': status_code,
                'type': 'User registered  successfully',
            }
            return Response(response, status=status_code)




class DMtextSet(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request): 
        user = request.user
        data = request.data  

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

        alldmtext = DMtextSetModel.objects.filter(Q(user=user)).values('pk', 'title50', 'title25', 'title10', 'text1000', 'text500', 'text250', 'text100', 'register_date', 'recent_send_date', 'sent_count', 'click_rate', 'total_count', 'average_count' )
        
        status_code = status.HTTP_200_OK
        response = {
            'success': 'True',
            'dmdata': alldmtext,
            'status code': status_code,
            'type': 'User registered  successfully',
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
            'type': 'User registered  successfully',
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
            'type': 'User registered  successfully',
        }

        return Response(response, status=status_code)




class EditedDmtextSave(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request): 
        user = request.user 
        data = request.data
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
            'type': 'User registered  successfully',
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

        status_code = status.HTTP_200_OK
        response = {
            'success': 'True',
            'data': data,
            'register_statu': register_statu,
            'status code': status_code,
            'type': 'User registered  successfully',
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
            'type': 'User registered  successfully',
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
            'type': 'User registered  successfully',
        }

        return Response(response, status=status_code)


class CsvImport(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        user = request.user 
        csvfile = request.FILES.get('csv', '') 
        fs = FileSystemStorage()
        filename = fs.save(csvfile.name, csvfile)
        filepath = fs.url(filename)
        empexceldata = pd.read_excel("."+filepath)
        
        responseData = []
        i = 1
        for dbframe in empexceldata.itertuples():  
 
            responseData.append({
                "id":i,
                "name":dbframe.企業名, 
                "mailaddress":dbframe.メール,
                "contact_url":dbframe.お問合せフォームURL,
                "site_url":dbframe.URL,
                "phone_num":dbframe.郵便番号,
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
        print(data['method'])
        if(data['method'] == '1'):            
            for d in data['data']: 
                print(d['corporate_name'])
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
            # print(data['data'])
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
            textpattern_temp.append({
                'pk':tp['pk'],
                'title50':tp['title50'],
                'title25':tp['title25'],
                'title10':tp['title10'],
                'text1000':tp['text1000']+"\n\n\n" + method.click_link +str(tp['pk']),
                'text500':tp['text500']+"\n\n\n" + method.click_link + str(tp['pk']),
                'text250':tp['text250']+"\n\n\n" + method.click_link + str(tp['pk']),
                'text100':tp['text100']+"\n\n\n" + method.click_link + str(tp['pk']),
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
        
        global interupt_flag, total_result 
        
        if(text_option == 1): #---------------------配信文章を選択
            if(data['send_date'] == 1): #-----------送信日時の設定
                if(data['send_method'] == 1): #-----送信方法を選択
                    sendDMAutoMatic(data, user, tpat1)

        if(text_option == 2): #---------------------配信文章を選択
            if(data['send_date'] == 1): #-----------送信日時の設定
                if(data['send_method'] == 1): #-----送信方法を選択
                    sendDMAutoMatic(data, user, tpat1)
                    sendDMAutoMatic(data, user, tpat2)

        
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


html_str = ""
form_datas = []
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
         
        global html_str, form_datas, site_url
        hs =  html_str
        fds = form_datas
        su = site_url

        html_str = ""
        form_datas = []
        site_url = ""

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
                user.expirydate = datetime.timedelta(30)
                user.save()
        if event_type == 'invoice.payment_failed':            
            user = User.objects.filter(Q(customer_id = request.data['data']['object']['customer'])).first()
             
        if event_type == 'customer.subscription.deleted':
            user = User.objects.filter(Q(customer_id = request.data['data']['object']['customer'])).first()
            if user: 
                user.paydate = None
                user.expirydate = None 
                user.customer_id = None
                user.subscription_id = None
                user.save()

        if event_type == 'payment_intent.succeeded':  
            print("request.data['data']: ", request.data['data'])    
            user = User.objects.filter(Q(customer_id = request.data['data']['object']['customer'])).first()
            if user: 
                user.initial_pay_statu = 1 
                user.save()

        return Response(json.dumps({'status': 'success'}))


class UserCreateSubscription(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        user = request.user
        data = request.data

        price_id = "" 
        if(data['plan'] == 0):
            price_id = settings.INITIAL_PRICE_ID
        if(data['plan'] == 1):
            price_id = settings.ECO_PRICE_ID
        if(data['plan'] == 2):
            price_id = settings.STANDARD_PRICE_ID
        if(data['plan'] == 3):
            price_id = settings.PRO_PRICE_ID
        if(data['plan'] == 4):
            price_id = settings.ENTERPISE_PRICE_ID

        stripe.api_key = settings.STRIPE_SECRET_KEY
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
                user.subscription_id = subscription.id
                user.save()
                status_code = status.HTTP_201_CREATED 
                response = {
                    'status': status_code,
                    'clientSecret': subscription.latest_invoice.payment_intent.client_secret
                } 

                return Response(response, status=status_code)
            except Exception as e: 
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
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



# =================================================
# 
# ----------ADMIN SIDE-----------------------------
# 
# =================================================



 
class IsAdmin(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request): 
        user = request.user      
        
        isadmin = 0

        if user.is_superuser == 1:
            isadmin = 1

        print(isadmin)
        status_code = status.HTTP_200_OK
        response = {
            'success': 'True', 
            'status code': status_code, 
            'isadmin':isadmin,
            'type': 'successfully',
        }
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
            'type': 'User registered  successfully',
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

    browser         = Browser()
    browser.set_handle_equiv(False)
    browser.set_handle_robots(False)
    browser.addheaders = [('User-agent','Mozilla/5.0 (X11; Linux x86_64; rv:18.0)Gecko/20100101 Firefox/18.0 (compatible;)'),('Accept', '*/*')]   
    
    global interupt_flag, total_result 

    for d in data['rows']:

        if(interupt_flag == True):
            break
        else:
            URL = d['contact_url']                                
            ContactMail = d['mailaddress']                                

            if(URL != ""):
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
                    continue

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
                    recaptID = requests.post("http://azcaptcha.com/in.php?key=ztjfvxqglrkygp9zx4mkh3bh7b6ccm2d&method=userrecaptcha&version=v3&action=verify&min_score=0.3&googlekey="+ sitekey +"&pageurl="+URL)
                    ds = BeautifulSoup(recaptID.content, "html.parser") 

                    recaptchResponse = requests.post("http://azcaptcha.com/res.php?key=ztjfvxqglrkygp9zx4mkh3bh7b6ccm2d&action=get&id="+str(ds).replace("OK|", ""))
                    rd = BeautifulSoup(recaptchResponse.content, "html.parser")

                    print(rd)
                # End reCaptcha sector

                #End Get Site Key

                form = soup.find('form') 
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
                        if(input['type'] == "email"):
                            browser[input['name']] = user.corporate_mail
                            key = input['name']
                            value = user.corporate_mail
                            formTempData[key] = value                                          

                        if(input['type'] == "text"):
                            browser[input['name']] = ''
                            key = input['name']
                            value = ""
                            formTempData[key] = value

                            if(input['name'].find("name") != -1 \
                            or r"user_name" in input['name'] \
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
                    if(interupt_flag == True):
                        break
                    else:
                        browser[textarea['name']] = tpattern['text1000']
                        key = textarea['name']
                        value = tpattern['text1000']
                        formTempData[key] = value 


                for select in selects: 
                    if(interupt_flag == True):
                        break
                    else:
                        option = select.select('option') 
                        browser[select['name']] = [option[0]['value']]
                        key = select['name']
                        value = option[0]['value']
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
                    content = response.read() 
                    soup = BeautifulSoup(content, "html.parser")  
                    form = soup.find('form')   
                    # print(form) 
                    if("失敗" in str(form) or "後でまたお試" in str(form) or "エラー" in str(form) or "問題があります" in str(form)):
                        total_result.append({"status":"fail", "data": d })  
                        # print(form)                  

                    else:
                        cuurl = response.geturl()
                        urlArr = cuurl.split("/")

                        urlFirst = ''
                        i = 0
                        for u in urlArr:
                            if(i < len(urlArr) - 1):
                                urlFirst = urlFirst + u + "/"
                            i = i + 1
        
                        naction = form['action'] 
                        
                        if(naction.find('./') != -1):
                            naction = naction.replace('./', "")   

                        if(naction.find('/') != -1):
                            naction = naction.replace('/', "")              
                        
                        comUrl = urlFirst + naction  

                        checkStr = soup.find_all("form")
                        checkStr = str(checkStr)

                        if "送信" in str(soup.find_all("form")) \
                            and "submit" in str(soup.find_all("form") \
                                or checkStr.count("修正する") > 0 \
                                    or checkStr.count("戻") > 0):
                        
                            cinputs = form.find_all('input') 
                            
                            for cd in cinputs:

                                if(cd['type'] == 'submit'):
                                    if( cd.has_attr('name')):
                                        key = cd['name']
                                        value = "submit button"
                                        formTempData[key] = value 
                                    else:
                                        key = ''
                                        value = "submit"
                                        formTempData[key] = value 
                            
                            request_ans = requests.post(comUrl, data=formTempData)    
                            ans_html = BeautifulSoup(request_ans.content, "html.parser") 
                            print("OK===================")                                     
                            total_result.append({"status":"success", "data": d }) 
                else:
                    req_data_str = str(rd)
                    if(req_data_str.count('ERROR') > 0 or req_data_str.count('CAPCHA_NOT_READY') > 0):
                        total_result.append({"status":"fail", "data": d }) 

                    else:
                        if(flag == False): 
                            formTempData['g-recaptcha-response'] = req_data_str
                            request_ans = requests.post(URL, data=formTempData)
                            ans_html = BeautifulSoup(request_ans.content, "html.parser") 
                            # print(ans_html) 
                            total_result.append({"status":"success", "data": d })                     

            if(ContactMail != "" and URL == ""):                
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

            if(ContactMail == "" and URL == ""):                
                total_result.append({"status":"fail", "data": d })



def reserveSendSubFunction(main_data, user, tpattern, browser, specific_day, reserve_date, tpattern1_s, tpattern2_s, text_option_s):
    URL = main_data['contact_url']                                
    ContactMail = main_data['mailaddress']                                
    subtotal_result = []

    if(URL != ""):
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
            recaptID = requests.post("http://azcaptcha.com/in.php?key=ztjfvxqglrkygp9zx4mkh3bh7b6ccm2d&method=userrecaptcha&version=v3&action=verify&min_score=0.3&googlekey="+ sitekey +"&pageurl="+URL)
            ds = BeautifulSoup(recaptID.content, "html.parser") 

            recaptchResponse = requests.post("http://azcaptcha.com/res.php?key=ztjfvxqglrkygp9zx4mkh3bh7b6ccm2d&action=get&id="+str(ds).replace("OK|", ""))
            rd = BeautifulSoup(recaptchResponse.content, "html.parser")

            print(rd)
        # End reCaptcha sector

        #End Get Site Key

        form = soup.find('form') 
        inputs = form.find_all('input') 
        textareas = form.find_all('textarea') 
        checkboxes = form.find_all(type = 'checkbox') 
        selects = form.select('select')    
        
        formTempData = {}    
        flag = False
            
        for input in inputs:                    
            if(input['type'] == "email"):
                browser[input['name']] = user.corporate_mail
                key = input['name']
                value = user.corporate_mail
                formTempData[key] = value                                          

            if(input['type'] == "text"):
                browser[input['name']] = ''
                key = input['name']
                value = ""
                formTempData[key] = value

                if(input['name'].find("name") != -1 \
                or r"user_name" in input['name'] \
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
            
            browser[textarea['name']] = tpattern['text1000']
            key = textarea['name']
            value = tpattern['text1000']
            formTempData[key] = value 


        for select in selects: 
            
            option = select.select('option') 
            browser[select['name']] = [option[0]['value']]
            key = select['name']
            value = option[0]['value']
            formTempData[key] = value   

        for checkbox in checkboxes:  
            
            checkbox.selected =True
            key = checkbox['name']
            value = True
            formTempData[key] = value 

        
        if(sitekey == ""):
            response = browser.submit()
            content = response.read() 
            soup = BeautifulSoup(content, "html.parser")  
            form = soup.find('form')   
            # print(form) 
            if("失敗" in str(form) or "後でまたお試" in str(form) or "エラー" in str(form) or "問題があります" in str(form)):
                subtotal_result.append({"status":"fail", "data": main_data })  
                # print(form)                  

            else:
                cuurl = response.geturl()
                urlArr = cuurl.split("/")

                urlFirst = ''
                i = 0
                for u in urlArr:
                    if(i < len(urlArr) - 1):
                        urlFirst = urlFirst + u + "/"
                    i = i + 1

                naction = form['action'] 
                
                if(naction.find('./') != -1):
                    naction = naction.replace('./', "")   

                if(naction.find('/') != -1):
                    naction = naction.replace('/', "")              
                
                comUrl = urlFirst + naction  

                checkStr = soup.find_all("form")
                checkStr = str(checkStr)

                if "送信" in str(soup.find_all("form")) \
                    and "submit" in str(soup.find_all("form") \
                        or checkStr.count("修正する") > 0 \
                            or checkStr.count("戻") > 0):
                
                    cinputs = form.find_all('input') 
                    
                    for cd in cinputs:

                        if(cd['type'] == 'submit'):
                            if( cd.has_attr('name')):
                                key = cd['name']
                                value = "submit button"
                                formTempData[key] = value 
                            else:
                                key = ''
                                value = "submit"
                                formTempData[key] = value 
                    
                    request_ans = requests.post(comUrl, data=formTempData)    
                    ans_html = BeautifulSoup(request_ans.content, "html.parser") 
                    print("OK===================")                                     
                    subtotal_result.append({"status":"success", "data": main_data }) 
        else:
            req_data_str = str(rd)
            if(req_data_str.count('ERROR') > 0 or req_data_str.count('CAPCHA_NOT_READY') > 0):
                subtotal_result.append({"status":"fail", "data": main_data }) 

            else:
                if(flag == False): 
                    formTempData['g-recaptcha-response'] = req_data_str
                    request_ans = requests.post(URL, data=formTempData)
                    ans_html = BeautifulSoup(request_ans.content, "html.parser") 
                    # print(ans_html) 
                    subtotal_result.append({"status":"success", "data": main_data })                     

    if(ContactMail != "" and URL == ""):                
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

        if(URL != ""):            
            page = requests.get(URL) 
            soup = BeautifulSoup(page.content, "html.parser")      
            
            global html_str, form_datas, site_url

            html_str = str(soup)            

            form = soup.find('form') 


            urlArr = URL.split("/")

            urlFirst = ''
            i = 0
            for u in urlArr:
                if(i < len(urlArr) - 1):
                    urlFirst = urlFirst + u + "/"
                i = i + 1

            naction = str(form['action'] )
            
            if(naction.find('./') != -1):
                naction = naction.replace('./', "")   

            if(naction.find('/') != -1):
                naction = naction.replace('/', "")              
            
            comUrl = urlFirst + naction  

            site_url = comUrl

            inputs = form.find_all('input') 
            textareas = form.find_all('textarea') 
            checkboxes = form.find_all(type = 'checkbox') 
            selects = form.select('select')    


            for input in inputs:                  
                if(input['type'] == "email"):                                                               
                    form_datas.append({"tag":"input", "name":input['name'], "value":user.corporate_mail})

                if(input['type'] == "text"):
                    if(input['name'].find("name") != -1 \
                    or r"user_name" in input['name'] \
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
                        
                        form_datas.append({"tag":"input", "name":input['name'], "value":user.firstname_of_charger + user.lastname_of_charger})
                       
                    if( "姓" == input['name'] \
                        or "firstName" == input['name'] \
                            or "first_name" == input['name'] \
                                or "name1" == input['name'] \
                                    or "FirstName" in input['name'] \
                                        or "firstname" in input['name'] ):  
                        form_datas.append({"tag":"input", "name":input['name'], "value":user.firstname_of_charger})                        
                        
                    if( "lastName" == input['name'] \
                        or "name2" == input['name'] \
                            or "名" == input['name'] \
                                or "LastName" == input['name'] \
                                    or "name3" in input['name'] \
                                        or "lastname" in input['name'] ): 
                        
                        form_datas.append({"tag":"input", "name":input['name'], "value":user.lastname_of_charger})   

                    if(input['name'].find("comp") != -1 \
                        or input['name'].find("cname") != -1 \
                        or "organization" in input['name'] \
                        or "your-company" in input['name'] \
                        or "company-name" in input['name'] \
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
                        
                        form_datas.append({"tag":"input", "name":input['name'], "value":user.coporate_name})                                                 

                    if(input['name'].find("post") != -1 or input['name'].find("add") != -1 \
                        or "your-post" in input['name'] \
                            or "zip" in input['name'] \
                                or "code" in input['name']):

                        form_datas.append({"tag":"input", "name":input['name'], "value":user.corporate_zipcode})   

                    if(input['name'].find("phon") != -1 \
                        or "tel" in input['name'] \
                            or "TEL" in input['name'] \
                                or "Tel" in input['name'] \
                                    or "電話" in input['name'] \
                                        or "phone" in input['name'] \
                                            or "Phone" in input['name']):  

                        form_datas.append({"tag":"input", "name":input['name'], "value":user.corporate_phone}) 
                        
                    if(input['name'].find("fax") != -1):
                        form_datas.append({"tag":"input", "name":input['name'], "value":user.corporate_fax})       

                    if(input['name'].find("subject") != -1):
                        form_datas.append({"tag":"input", "name":input['name'], "value":tpattern['title50']})          
                    
                    if(input['name'].find("mail") != -1): 
                        form_datas.append({"tag":"input", "name":input['name'], "value":user.corporate_mail})  

                    if(input['name'].find("furigana") != -1 \
                        or "your-furiga" in input['name'] \
                            or "userfuriga" in input['name'] \
                                or "personal_furigana_name" in input['name'] \
                                    or "name_ruby" in input['name'] \
                                        or "ふりがな" in input['name'] ): 
                        
                        form_datas.append({"tag":"input", "name":input['name'], "value":user.firstname_of_charger_firagana + user.lastname_of_charger_firagana})  
                         
                    if(input['name'] == "quiz-31"): 
                        form_datas.append({"tag":"input", "name":input['name'], "value":"東京"})   
                    
                if(input['type'] == "tel"):
                    if(input['name'].find("phon") != -1 \
                        or "tel" in input['name'] \
                            or "TEL" in input['name'] \
                                or "Tel" in input['name'] \
                                    or "電話" in input['name'] \
                                        or "phone" in input['name'] \
                                            or "Phone" in input['name']):   
                        form_datas.append({"tag":"input", "name":input['name'], "value":user.corporate_phone})
                        

                    if(input['name'].find("post") != -1 \
                        or "your-post" in input['name'] \
                            or "postalCode" in input['name'] \
                                or "zip" in input['name']):

                        form_datas.append({"tag":"input", "name":input['name'], "value":user.corporate_zipcode}) 
                
                if(input['type'] == "radio"):  
                    form_datas.append({"tag":"input", "name":input['name'], "value":"radio"}) 

            for textarea in textareas:  
                form_datas.append({"tag":"textarea", "name":textarea['name'], "value":tpattern['text1000']})                             

            for select in selects: 
                form_datas.append({"tag":"select", "name":select['name'], "value":"select"})     
                               

            for checkbox in checkboxes:   
                form_datas.append({"tag":"checkbox", "name":checkbox['name'], "value":"checkbox"})                 
             

