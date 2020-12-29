from django.test import TestCase
from bank import models
from core.models import Account


def sample_account(**params):
    defaults = {
        'pk': 88,
        'name': 'coca-cola',
        'vat': '1234568555',
        'business_id': 'kskajajja'
    }
    defaults.update(params)

    return Account.objects.create(**defaults)


class ModelTests(TestCase):

    def test_client_str(self):
        acc = sample_account()
        acc.save()
        klient = models.Clients.objects.create(
            account=acc,
            name='GradinG',
            vat='1234546',
            business_id='m8faas99'
        )
        self.assertEqual(str(klient), klient.name)
