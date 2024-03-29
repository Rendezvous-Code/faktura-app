from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_user(user, **params):
    user = get_user_model()
    defaults = {
        'email': 'coca-cola@test.rs',
        'pass': 'test1234568555',
    }
    defaults.update(params)

    return user.objects.create(user, **defaults)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        email = 'test@rendezvous.rs'
        password = 'Testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        email = 'test@RENDEZVOUS.RS'
        user = get_user_model().objects.create_user(email, 'tests1as')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test1234')

    def test_create_new_superuser(self):
        user = get_user_model().objects.create_superuser(
            'test@rendezvous.rs',
            'test12345'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_account_str(self):
        account = models.Account.objects.create(
            name='Renedezvous Code',
            vat='234567891011',
            business_id='159875321'
        )

        self.assertEqual(str(account), account.name)
