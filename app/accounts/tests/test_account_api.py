from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Account


CREATE_ACCOUNT_URL = reverse('account:create')


def sample_account(**params):
    defaults = {
        'name': 'coca-cola',
        'vat': '1234568555',
        'business_id': 'kskajajja'
    }
    defaults.update(params)

    return Account.objects.create(**defaults)


class PublicAccountApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_account(self):
        payload = {
            'name': 'pepsi',
            'vat': '1234568575',
            'business_id': '785232154'
        }
        res = self.client.post(CREATE_ACCOUNT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        account = Account.objects.get(**res.data)
        self.assertEqual(account.id, 1)

    def test_account_exists(self):
        """Test creating account that already exists fails"""
        payload = {
            'name': 'sveps',
            'vat': '1884568575',
            'business_id': '7855532154'
        }
        sample_account(**payload)
        res = self.client.post(CREATE_ACCOUNT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_toke_missing_field(self):
        """Test that vat and business_id are required"""
        res = self.client.post(CREATE_ACCOUNT_URL,
                               {'name': 'rndvs', 'vat': '', 'business_id': ''})

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
