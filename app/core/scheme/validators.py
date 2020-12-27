from django.core.exceptions import ValidationError
from jsonschema import validate
from core.scheme.account_schema import ACCOUNT_SETTINGS_SCHEMA


def _validate_json_schema(value, schema):
    try:
        validate(instance=value, schema=schema)
    except Exception as e:
        raise ValidationError(str(e))


def validate_account_settings(value):
    _validate_json_schema(value, ACCOUNT_SETTINGS_SCHEMA)
