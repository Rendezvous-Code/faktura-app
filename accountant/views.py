from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Account
from accountant import serializers


class AccountViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Manage account in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Account.objects.all()
    serializer_class = serializers.AccountSerializer
