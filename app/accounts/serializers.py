from rest_framework import serializers
from core.models import Account


class AccountSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""
    # user = serielizers.PrimaryKeyRelatedField(many=False, Users?

    class Meta:
        model = Account
        fields = ('pk', 'id', 'name', 'vat', 'business_id')
        read_only_fields = ('id', 'pk')

    def create(self, validated_data):
        """create new account return it"""
        account = Account.objects.create(**validated_data)
        account.save()
        return account
