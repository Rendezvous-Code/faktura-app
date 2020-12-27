from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin
from core.scheme.validators import validate_account_settings


class Timestamps(models.Model):
    """
    Abstract model representing keeping track of object construction
    and editing times.
    """
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='Autopopulated timestamp of object creation time.')
    modified_at = models.DateTimeField(
        auto_now=True,
        help_text='Autopopulated timestamp of last object modification time.')

    class Meta:
        abstract = True


class Permission(models.Model):
    """Model for set permissions for any other Model."""

    name = models.CharField(
        max_length=50,
        help_text='The package of permission',)

    action = models.CharField(
        max_length=50,
        help_text='The action of permission')

    namespace = models.JSONField(
        help_text='Field url namespaces',
        blank=True, null=True,
    )

    method = models.CharField(
        max_length=50,
        help_text='The action of permission')

    class Meta:
        unique_together = ('name', 'action')

    def __str__(self):
        return "{}-{}".format(self.name, self.action)

    ADMIN_DISPLAY = ['id', 'name', 'action']


class PermissionGroup(models.Model):
    name = models.CharField(
        max_length=50,
        help_text='The package of permission',
        unique=True
    )
    permissions = models.ManyToManyField(Permission,
                                         related_name='group_permisions')

    def __str__(self):
        return "{}".format(self.name)

    ADMIN_DISPLAY = ['id', 'name']


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model"""
    email = models.EmailField(max_length=255, unique=True)
    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'


class Account(models.Model):
    """
    Model used to save data about an account.

    If a client is using only a single account, all of its users (having either
    'account-admin' or 'account-user' roles) should belong to the said account.
    """

    name = models.CharField(
        max_length=128,
        help_text='Name for the account')
    vat = models.CharField(
        max_length=128,
        help_text='VAT number',
        unique=True,
        blank=False,
        null=False
    )
    business_id = models.CharField(
        max_length=128,
        help_text='Company ID number',
        unique=True,
        blank=False,
        null=False
    )
    settings = models.JSONField(
        help_text='Account settings in JSON format.',
        null=True, blank=True,
        validators=[validate_account_settings])

    ADMIN_DISPLAY = ['name', 'vat', 'business_id']

    def __str__(self):
        """Model representation (used in admin)."""
        return self.name

    def max_members(self):
        default = settings.MIN_NUMBER_OF_ACCOUNT_MEMBERS
        if self.settings is not None:
            return self.settings.get('max_number_of_account_members', default)
        return default

    def get_effective_settings(self):
        all_settings = {}
        settings_json = self.settings
        if settings_json is not None:
            all_settings = settings_json
        return all_settings

    @property
    def admins(self):
        return UserProfile.objects.filter(
            account=self,
            group_permisions__name='account-admin',
            user__is_active=True,
        )


class UserProfile(models.Model):
    """A user profile (way to extend Django's user object)."""

    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='user_profile')

    account = models.ManyToManyField(
        Account,
        help_text='Account this user belongs to.',
        related_name="user_accounts"
    )

    permissions = models.ManyToManyField(
        Permission,
        related_name='user_permisions',
        blank=True)
    group_permisions = models.ManyToManyField(
        PermissionGroup,
        related_name='user_group_permisions',
        blank=True
    )

    ADMIN_DISPLAY = ['user', 'groups', 'accounts']

    def accounts(self):
        return ", ".join(str(v) for v in self.account.all())

    def all_accounts(self):
        return self.account.all()

    def groups(self):
        return ", ".join(str(v) for v in self.group_permisions.all())

    def __str__(self):
        """Model representation (used in admin)."""
        return self.user.email

    def account_role(self):
        """
        Find a user role for the account member
        """
        from core.utils import ACCOUNT_PERMISSION_GROUPS
        account_groups = list(filter(lambda x: x.name.startswith('account-'),
                                     self.group_permisions.all()))

        if len(account_groups) > 0:
            group = account_groups[0]
            role = next(g for g in ACCOUNT_PERMISSION_GROUPS
                        if g['name'] == group.name)
            return role['str']
        return 'undefined'

    def account_status(self):
        """
        Platform user status
        """
        if not self.user.has_usable_password():
            return 'Pending'  # pending invite
        elif self.user.is_active:
            return 'Active'
        else:
            return 'Access disabled'

    def _permission_groups_list(self):
        return list(self.group_permisions.all().values_list('name', flat=True))

    @property
    def is_account_admin(self):
        return 'account-admin' in self._permission_groups_list()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, raw, **kwargs):
    """Automatically create the profile when user object is created."""
    # post_save signal should be disabled when ``raw=True``
    # (i.e. when loading a test fixture). For details, please see:
    # https://docs.djangoproject.com/en/1.11/ref/signals/#post-save for details
    if raw:
        return

    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, raw, **kwargs):
    """Automatically save the profile when user object is edited."""
    # post_save signal should be disabled when ``raw=True``
    # (i.e. when loading a test fixture). For details, please see:
    # https://docs.djangoproject.com/en/1.11/ref/signals/#post-save for details
    if raw:
        return

    instance.user_profile.save()
