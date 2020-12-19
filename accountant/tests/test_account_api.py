from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Account
# from accountant.serializers import AccountSerializer

ACCOUNTS_URL = reverse('accountant:account-list')


class PublicAccountApiTest(TestCase):
    """Test the publicly available accounts API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for getting account list"""
        res = self.client.get(ACCOUNTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateAccountApiTest(TestCase):
    """Test the authorized user account API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@rendezvous.rs',
            'password123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_account(self):
        """Test retreiving accounts"""
        Account.objects.create(name='Agencija 1', details=[])
        Account.objects.create(name='Agencija 2', details=[])

        res = self.client.get(ACCOUNTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
