from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from bank.models import Clients, OwnerBankAccount, ClientBankAccount
from core.models import Account


class ClientSerializer(serializers.ModelSerializer):
    """Serializer for the clients object"""
    account = serializers.PrimaryKeyRelatedField(
        queryset=Account.objects.all())

    class Meta:
        model = Clients
        fields = ('id', 'name', 'vat', 'business_id', 'account')
        read_only_fields = ('id',)

    def create(self, validated_data):
        """create new user with encrypted password and return it"""
        klijent = Clients.objects.create(**validated_data)
        klijent.save()
        return klijent

    # def update(self, instance, validated_data):
    #    """Update a user, setting the password correctly and return it"""
    #    password = validated_data.pop('password', None)
    #    klijent = super().update(instance, validated_data)

    #    return klijent


class OwnerBankAccountSerializer(serializers.ModelSerializer):
    """Serializer for the owner bank account object"""
    account = serializers.PrimaryKeyRelatedField(
        queryset=Account.objects.all())

    class Meta:
        model = OwnerBankAccount
        fields = ('id', 'name', 'bank', 'account_number', 'amount', 'account')
        read_only_fields = ('id',)

    def create(self, validated_data):
        """create new user with encrypted password and return it"""
        bank_acc = OwnerBankAccount.objects.create(**validated_data)
        bank_acc.save()
        return bank_acc


class ClientBankAccountSerializer(serializers.ModelSerializer):
    """Serializer for the clients bank account object"""
    klient = serializers.PrimaryKeyRelatedField(
        queryset=Clients.objects.all())

    class Meta:
        model = ClientBankAccount
        fields = ('id', 'name', 'bank', 'account_number', 'amount', 'klient')
        read_only_fields = ('id',)

    def create(self, validated_data):
        """create new user with encrypted password and return it"""
        bank_acc = ClientBankAccount.objects.create(**validated_data)
        bank_acc.save()
        return bank_acc
