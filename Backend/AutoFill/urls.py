from django.urls import path
from Backend.AutoFill.views import UserRegisterView, UserLoginView, VerifyEmail, ResendVerifyEmailCode, BasicInfoRegisteration, SendMailSetting, \
    AddStopLinks, DmClickedCountCalculation, Maildeliverystoptext, MesurmentMethodSet, Getmesurmentmethodsetting, DMtextSet, GetDMAlltextdata, \
    Copydmtextrows, Deletedmtextrows, EditedDmtextSave, GetAllDMGroupData, SaveAllDMGroupData, Deletdmgroup, CsvImport, DMlistsSave, GetAllDMlists, \
    Deletedmlists, SaveEditedListdata, AddDMLists, GetFormData, GetGroupAndTextPattern, InterruptSendDM, ManualSendDM, Stopcsvimport, GetAllStoplists, \
    Deletestoplist, GetallStatus, GetallUsers, UserCreateSubscription, GetPaymentStatus, SavePaymentMethod, SavePricePlan, CreateCheckoutSessionView, \
    UpdateAccountInfo, GetBasicInfo, SetOptionPrice, WebhookView, UpdateSubscription, SetPaymentasBank, AdminLoginView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('register', UserRegisterView.as_view()), 
    path('updateaccount', UpdateAccountInfo.as_view()), 
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
    path('dmtextset', DMtextSet.as_view()),
    path('getalldmtextdata', GetDMAlltextdata.as_view()),
    path('copydmtextrows', Copydmtextrows.as_view()),
    path('deletedmtextrows', Deletedmtextrows.as_view()),   
    path('editeddmtextsave', EditedDmtextSave.as_view()),    
    path('getalldmgroupdata', GetAllDMGroupData.as_view()),    
    path('savealldmgroupdata', SaveAllDMGroupData.as_view()),    
    path('deletdmgroup', Deletdmgroup.as_view()),    
    path('csvimport', CsvImport.as_view()),    
    path('stopcsvimport', Stopcsvimport.as_view()),    
    path('dmlistssave', DMlistsSave.as_view()),    
    path('getalldmlists', GetAllDMlists.as_view()),    
    path('getallstoplist', GetAllStoplists.as_view()),    
    path('deletedmlists', Deletedmlists.as_view()),    
    path('deletestoplist', Deletestoplist.as_view()),    
    path('saveEditedListdata', SaveEditedListdata.as_view()),  
    path('adddmists', AddDMLists.as_view()),  
    path('startsendmessage', GetFormData.as_view()),    
    path('getalldmlists_dmtexts', GetGroupAndTextPattern.as_view()),    
    path('interrupt', InterruptSendDM.as_view()),    
    path('startsendmessage_bymanual', ManualSendDM.as_view()),    
    path('getallstatus', GetallStatus.as_view()),    
    path('getallusers', GetallUsers.as_view()),    
    path('usercreatesubscription', UserCreateSubscription.as_view()),    
    path('createcheckoutsession', CreateCheckoutSessionView.as_view()),
    path('getpaymentstatu_getpagedata', GetPaymentStatus.as_view()),    
    path('savepaymentmethod', SavePaymentMethod.as_view()),    
    path('savepriceplan', SavePricePlan.as_view()),   
    path('setoptionprice', SetOptionPrice.as_view()),        
    path('getbasicinfo', GetBasicInfo.as_view()),  
    path('updatepricceplan', UpdateSubscription.as_view()), 
    path('webhook', WebhookView.as_view()),    
    path('setPaymentasBank', SetPaymentasBank.as_view()),    
    

    # Admin part
    path('admin_login', AdminLoginView.as_view()), 





    path('login/token/refresh/',TokenRefreshView.as_view(),name="token_refresh"),
    path('login/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
]


