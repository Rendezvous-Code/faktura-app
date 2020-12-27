"""
JSON schema for the account settings
"""
from django.conf import settings


ACCOUNT_SETTINGS_SCHEMA = {
    'type': 'object',
    'properties': {
        'max_number_of_account_members': {
            'type': 'integer',
            'minimum': settings.MIN_NUMBER_OF_ACCOUNT_MEMBERS,
            'exclusiveMaximum': settings.MAX_NUMBER_OF_ACCOUNT_MEMBERS
        },
    },
    'required': ['max_number_of_account_members', ]
}
