from rest_framework import serializers
from core.models import Account


class AccountSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""
    # user = serielizers.PrimaryKeyRelatedField(many=False, Users?

    class Meta:
        model = Account
        fields = ('id', 'name', 'vat', 'business_id')
        read_only_fields = ('id',)

    def create(self, validated_data):
        """create new account return it"""
        return Account.objects.create(**validated_data)
