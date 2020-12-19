from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                                    PermissionsMixin
# from django.conf import settings
import jsonfield


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves new user"""
        if not email:
            raise ValueError('Users must have email adress')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
  """Custom user model that supports using email instead of username"""
  email = models.EmailField(max_length=255, unique=True)
  name = models.CharField(max_length=255)
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)

  objects = UserManager()

  USERNAME_FIELD = 'email'


class Account(models.Model):
  """
  Account represents a client of our SaaS.

  An account can have multiple Entities associated with it.

  """
  name = models.CharField(
    max_length=128,
    help_text='Human readable account name (like "Coca Cola")')

  details = jsonfield.JSONField(
    max_length=100 * 1024,
    help_text='JSON-encoded content'
  )
  #   key = models.UUIDField(default=uuid.uuid4, editable=False)

  ADMIN_DISPLAY = ['name', 'get_owner', 'get_company', 'is_confirmed']

  def __str__(self):
    return self.name

  #   def get_current_subscription(self):
  #    subscriptions = self.subscriptions.all()
  #    if len(subscriptions) == 0:
  #        return None
  #    return subscriptions[0]

  def get_owner(self):
    return self.details.get('owner_name', None)

  get_owner.short_description = 'Owner'

  def get_company(self):
    return self.details.get('company_name', None)

  get_company.short_description = 'Company'

  def get_owner_email(self):
    return self.details.get('owner_email', None)

  def get_company_address(self):
    return self.details.get('company_address', None)

  def get_vat_number(self):
    return self.details.get('vat_number', None)

  def get_company_registration_number(self):
    return self.details.get('company_registration_number', None)

  def is_confirmed(self):
    return self.details.get('confirmed', None)

  is_confirmed.boolean = True


class AccountUser(models.Model):
  user = models.ForeignKey(
    User,
    on_delete=models.CASCADE)
  account = models.ForeignKey(
    Account,
    on_delete=models.CASCADE)
  is_account_owner = models.BooleanField(default=False)
  is_account_admin = models.BooleanField(default=False)
  disabled = models.BooleanField(default=False)

  ADMIN_DISPLAY = [
    'user', 'account',
    'is_account_owner',
    'is_account_admin',
    'has_password',
    'token'
  ]
  ADMIN_FILTER = ['is_account_admin', 'is_account_owner']
  ADMIN_SEARCH = ['account__name']
  ADMIN_READONLY = ['user', 'account']

  class Meta:
    unique_together = [('user', 'account')]


class Entity(models.Model):
  """Business entity model"""
  account = models.ForeignKey(
    Account,
    on_delete=models.CASCADE)
  name = models.CharField(max_length=255)
  id_number = models.CharField(max_length=60)
  vat = models.CharField(max_length=60)

  def __str__(self):
    return self.name


class BankAaccount(models.Model):
  """Bank account tied to Entity"""
  owner = models.ForeignKey(
    Entity,
    on_delete=models.CASCADE)
  name = models.CharField(max_length=255)
  bank_name = models.CharField(max_length=255)
  bank_account_number = models.CharField(max_length=255)

  def __str__(self):
    return self.bank_account_number


class Transaction(models.Model):
  account_number = models.ForeignKey(
    BankAaccount,
    on_delete=models.CASCADE)
  payment_code = models.CharField(max_length=3)
  purpose = models.CharField(max_length=255)
  debt = models.CharField(max_length=255, blank=True)
  credit = models.CharField(max_length=255, blank=True)
  beneficiary = models.CharField(max_length=255)
  beneficiary_acc_no = models.CharField(max_length=255, blank=True)
  receipt_date = models.CharField(max_length=30)

  def __str__(self):
    return self.purpose

  def get_ammount(self):
    if self.debt:
      return self.debt
    else:
      return self.credit
