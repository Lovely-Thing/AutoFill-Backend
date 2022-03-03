import uuid
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core import mail
from django.db import models
from django.conf import settings
import stripe


# User management
class UserManager(BaseUserManager):
  
    def create_user(self, email, password=None):
        """
        Create and return a `User` with an email, username and password.
        """
        if not email:
            raise ValueError('Users Must Have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(email, password)
        user.is_superuser = True
        stripe.api_key = settings.STRIPE_SECRET_KEY
        customer = stripe.Customer.create(
            description="AutoFill customer",
            email = user.email,
            metadata ={
                'point':0
            },
            name = "amdin"
        )
        user.customer_id = customer.id
        user.save()
        return user


class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True
        )
    password = models.CharField(max_length=255, unique=False, blank=False, null=False)
    coporate_name =  models.CharField(max_length=50, unique=False, blank=True, null=True)
    company_type =  models.CharField(max_length=50, unique=False, blank=True, null=True)
    corporate_furigana =  models.CharField(max_length=50, unique=False, blank=True, null=True)
    corporate_zipcode =  models.CharField(max_length=50, unique=False, blank=True, null=True)
    corporate_country =  models.CharField(max_length=200, unique=False, blank=True, null=True)
    corporate_prefecture =  models.CharField(max_length=50, unique=False, blank=True, null=True)
    corporate_city =  models.CharField(max_length=50, unique=False, blank=True, null=True)
    corporate_address =  models.CharField(max_length=50, unique=False, blank=True, null=True)
    corporate_building_name =  models.CharField(max_length=50, unique=False, blank=True, null=True)
    corporate_address_room_number =  models.CharField(max_length=50, unique=False, blank=True, null=True)
    corporate_estable_date =  models.CharField(max_length=50, unique=False, blank=True, null=True)
    corporate_phone =  models.CharField(max_length=50, unique=False, blank=True, null=True)
    corporate_fax =  models.CharField(max_length=50, unique=False, blank=True, null=True)
    corporate_mail =  models.CharField(max_length=50, unique=False, blank=True, null=True)
    corporate_homepage =  models.CharField(max_length=50, unique=False, blank=True, null=True)
    firstname_of_charger =  models.CharField(max_length=50, unique=False, blank=True, null=True)
    lastname_of_charger =  models.CharField(max_length=50, unique=False, blank=True, null=True)
    firstname_of_charger_firagana =  models.CharField(max_length=50, unique=False, blank=True, null=True)
    lastname_of_charger_firagana =  models.CharField(max_length=50, unique=False, blank=True, null=True)
    charger_prefecture =  models.CharField(max_length=50, unique=False, blank=True, null=True)
    charger_phone =  models.CharField(max_length=50, unique=False, blank=True, null=True)
    choice_word =  models.CharField(max_length=50, unique=False, blank=True, null=True)
    verificationcode = models.CharField(max_length=50, unique=False, blank=True, null=True)
    avatar =  models.CharField(max_length=255, unique=False, blank=True, null=True)
    userstatus = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    subscription_id = models.CharField(max_length=255, blank=True, null=True)
    customer_id = models.CharField(max_length=255, blank=True, null=True)
    paydate = models.DateTimeField(blank=True, null=True)
    expirydate = models.DateTimeField(blank=True, null=True)
    account_statu = models.IntegerField(default=0)
    price_plan = models.IntegerField(default=1)
    option_price = models.BooleanField(default=False)
    payment_method = models.IntegerField(default=1)
    initial_pay_statu = models.IntegerField(default=0)
    initial_pay_id = models.CharField(max_length=255, blank=True, null=True)
    total_send_count = models.IntegerField(default=0)
    total_send_success_count = models.IntegerField(default=0)
    total_send_faild_count = models.IntegerField(default=0)
    total_mail_send_count = models.IntegerField(default=0)
    total_inquiry_send_count = models.IntegerField(default=0) 
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    is_superuser = models.BooleanField(default=False)

    # Tells Django that the UserManager class defined above should manage
    # objects of this type.
    objects = UserManager()
    def __str__(self):
        return self.email

    class Meta:
        db_table = "User"


class SendMailSettingModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    name =  models.CharField(max_length=50, unique=False, blank=True, null=True)
    sendmail =  models.CharField(max_length=50, unique=False, blank=True, null=True) 
    replytodmail =  models.CharField(max_length=50, unique=False, blank=True, null=True) 
    smtp =  models.CharField(max_length=50, unique=False, blank=True, null=True) 
    mailid =  models.CharField(max_length=50, unique=False, blank=True, null=True) 
    mailpwd =  models.CharField(max_length=50, unique=False, blank=True, null=True) 
    mailport =  models.CharField(max_length=50, unique=False, blank=True, null=True) 
    mailssl =  models.CharField(max_length=50, unique=False, blank=True, null=True) 
    popcheck =  models.CharField(max_length=50, unique=False, blank=True, null=True) 
    popserver =  models.CharField(max_length=50, unique=False, blank=True, null=True) 
    username =  models.CharField(max_length=50, unique=False, blank=True, null=True) 
    userpwd =  models.CharField(max_length=50, unique=False, blank=True, null=True) 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='send_mail_setting')



class StopLinkSettingModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    name =  models.CharField(max_length=50, unique=False, blank=True, null=True)
    mailaddress =  models.CharField(max_length=50, unique=False, blank=True, null=True) 
    contact_url =  models.CharField(max_length=50, unique=False, blank=True, null=True) 
    site_url =  models.CharField(max_length=50, unique=False, blank=True, null=True) 
    phone_num =  models.CharField(max_length=50, unique=False, blank=True, null=True) 
    auto_manual =  models.CharField(max_length=50, unique=False, blank=True, null=True)  
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stop_link_setting')



class DmClickedCountModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    clickednum =  models.IntegerField(default=0)
    mailid = models.CharField(max_length=50, unique=False, blank=True, null=True) 



class MailDeliveryStopTextsModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  
    text2000 =  models.CharField(max_length=150, unique=False, blank=True, null=True)   
    text1000 =  models.CharField(max_length=150, unique=False, blank=True, null=True)   
    text500 =  models.CharField(max_length=150, unique=False, blank=True, null=True)   
    text250 =  models.CharField(max_length=150, unique=False, blank=True, null=True)   
    text100 =  models.CharField(max_length=150, unique=False, blank=True, null=True)   
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stop_text_setting')



class MesurmentMethodSettingModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  
    mesurment_method =  models.IntegerField(default=0)   
    click_link =  models.TextField(unique=False, blank=True, null=True)  
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mesurment_setting')



class DMtextSetModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  
    title50 =  models.TextField(unique=False, blank=True, null=True) 
    title25 =  models.TextField(unique=False, blank=True, null=True) 
    title10 =  models.TextField(unique=False, blank=True, null=True) 
    text1000 =  models.TextField(unique=False, blank=True, null=True)  
    text500 =  models.TextField(unique=False, blank=True, null=True)  
    text250 =  models.TextField(unique=False, blank=True, null=True)  
    text100 =  models.TextField(unique=False, blank=True, null=True)  
    register_date =  models.CharField(max_length=50, unique=False, blank=True, null=True) 
    recent_send_date =  models.CharField(max_length=50, unique=False, blank=True, null=True)     
    sent_count =  models.FloatField(default=0)    
    click_rate =  models.FloatField(default=0)    
    total_count =  models.FloatField(default=0)    
    average_count =  models.FloatField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dmtext_setting')


class DMGroupModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  
    title =  models.CharField(max_length=150, unique=False, blank=True, null=True)  
    subjectcount =  models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dmgroup')



class PerDMGroupDmListModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  
    name =  models.CharField(max_length=50, unique=False, blank=True, null=True)
    mailaddress =  models.CharField(max_length=50, unique=False, blank=True, null=True) 
    contact_url =  models.CharField(max_length=50, unique=False, blank=True, null=True) 
    site_url =  models.CharField(max_length=50, unique=False, blank=True, null=True) 
    phone_num =  models.CharField(max_length=50, unique=False, blank=True, null=True) 
    auto_manual =  models.CharField(max_length=50, unique=False, blank=True, null=True)  
    last_sent_user =  models.CharField(max_length=50, unique=False, blank=True, null=True) 
    last_sent_date =  models.CharField(max_length=50, unique=False, blank=True, null=True)  
    dmgroup = models.ForeignKey(DMGroupModel, on_delete=models.CASCADE, related_name='dm_group')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='per_dmgroup_list')



class DMSendStatusModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  
    data =  models.TextField(unique=False, blank=True, null=True)
    textpattern1 =  models.TextField(unique=False, blank=True, null=True)
    textpattern2 =  models.TextField(unique=False, blank=True, null=True)
    text_option =  models.IntegerField(default=0)
    status =  models.CharField(max_length=50, unique=False, blank=True, null=True)  
    reserve_date =  models.DateTimeField(unique=False, blank=True, null=True)  
    specific_day =  models.TextField(unique=False, blank=True, null=True)  
    list_table_id =  models.TextField(unique=False, blank=True, null=True)  
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dm_send_status')


class BillingModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  
    initial_amount =  models.FloatField(blank=True, null=True)
    monthly_amount =  models.FloatField(blank=True, null=True)
    initial_pay_date = models.DateTimeField(blank=True, null=True)
    monthly_pay_date = models.DateTimeField(blank=True, null=True)
    edit_date = models.DateTimeField(blank=True, null=True)
    editer = models.CharField(max_length=200, unique=False, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='billing_user')

