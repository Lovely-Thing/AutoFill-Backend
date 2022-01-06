import uuid
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
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
    corporate_country =  models.CharField(max_length=50, unique=True, blank=True, null=True)
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
    customer_id = models.CharField(max_length=50, unique=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
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