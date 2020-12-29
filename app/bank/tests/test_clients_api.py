from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from bank.models import Clients
from core.models import Account, UserProfile
from bank.serializers import ClientSerializer


CLIENTS_URL = reverse('bank:clients-list')


def sample_client(account, **params):
    defaults = {
        'name': 'WildBoars',
        'vat': '123456',
        'business_id': '7891011'
    }
    defaults.update(params)
    return Clients.objects.create(account=account, **defaults)


class PublicClientApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(CLIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateClientApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user1 = get_user_model().objects.create_user(
            email='test1@rendezvous.rs',
            password='testpass'
        )
        self.user2 = get_user_model().objects.create_user(
            email='test2@rendezvous.rs',
            password='testpass'
        )
        self.account1 = Account.objects.create(
            name='GradinG',
            vat='123456789',
            business_id='13456w5234'
        )
        self.account2 = Account.objects.create(
            name='Vitorog',
            vat='12345678889',
            business_id='1344456w5234'
        )
        self.user_profile1 = UserProfile.objects.create(
            user=self.user1,
            account=self.account1,
            is_account_admin=True,
            is_account_owner=True
        )
        self.user_profile2 = UserProfile.objects.create(
            user=self.user2,
            account=self.account2,
            is_account_admin=False,
            is_account_owner=False
        )

        self.client.force_authenticate(self.user1)

    def test_retrieve_clients(self):
        sample_client(account=self.account1)
        sample_client(account=self.account1)

        res = self.client.get(CLIENTS_URL)
        clients = Clients.objects.all().order_by('id')
        serializer = ClientSerializer(clients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_clients_limited_to_user(self):

        sample_client(account=self.account2)
        sample_client(account=self.account1)

        res = self.client.get(CLIENTS_URL)
        up = UserProfile.objects.get(user=self.user1)
        clients = Clients.objects.filter(account=up.account)
        serilazer = ClientSerializer(clients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serilazer.data)
