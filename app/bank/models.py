from django.db import models
from core.models import Account


class BaseBankAccount(models.Model):
    name = models.CharField(
        max_length=128,
        help_text='Name for the account')
    bank = models.CharField(
        max_length=128,
        help_text='Bank that holds account',
        blank=False,
        null=False
    )
    account_number = models.CharField(
        max_length=128,
        help_text='bank acount',
        unique=True,
        blank=False,
        null=False
    )
    amount = models.DecimalField(
        max_digits=64,
        decimal_places=2,
        help_text='Avaiable amount',
        default=0.00
    )


class OwnerBankAccount(BaseBankAccount):
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        help_text='Account this bank account belongs to.',
        related_name="company_account"
    )

    def __str__(self):
        """Model representation (used in admin)."""
        return self.name


class Clients(models.Model):
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        help_text='Account this client belongs to.',
        related_name="account_owner"
    )

    name = models.CharField(
        max_length=128,
        help_text='Name for the account')
    vat = models.CharField(
        max_length=128,
        help_text='VAT number',
        blank=False,
        null=False
    )
    business_id = models.CharField(
        max_length=128,
        help_text='Company ID number',
        blank=False,
        null=False
    )

    def __str__(self):
        """Model representation (used in admin)."""
        return self.name


class ClientBankAccount(BaseBankAccount):
    klient = models.ForeignKey(
        Clients,
        on_delete=models.CASCADE,
        help_text='Account this bank account belongs to.',
        related_name="company_account"
    )

    def __str__(self):
        """Model representation (used in admin)."""
        return self.name
