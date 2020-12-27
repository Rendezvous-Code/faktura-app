from rest_framework import generics
from accounts.serializers import AccountSerializer


class CreateAccountView(generics.CreateAPIView):
    """Manage Accounts in Database"""
    serializer_class = AccountSerializer
