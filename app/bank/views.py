from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from bank.models import Clients
from core.models import UserProfile
from bank import serializers


class ClientViewSet(viewsets.ModelViewSet):
    """Manage clients in db"""
    serializer_class = serializers.ClientSerializer
    queryset = Clients.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrieve the clients for auth user"""
        user_profile = UserProfile.objects.get(user=self.request.user)
        return self.queryset.filter(account=user_profile.account)
