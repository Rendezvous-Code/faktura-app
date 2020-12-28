from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from core.models import Account, UserProfile


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    class Meta:
        model = get_user_model()
        fields = ('id', 'pk', 'email', 'password', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}
        read_only_fields = ('id', 'pk')

    def create(self, validated_data):
        """create new user with encrypted password and return it"""
        user = get_user_model().objects.create_user(**validated_data)
        user.save()
        return user

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()
        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for the User Profile object"""
    user = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all())
    account = serializers.PrimaryKeyRelatedField(
        queryset=Account.objects.all())

    class Meta:
        model = UserProfile
        fields = ('user', 'account', 'is_account_owner', 'is_account_admin')

    def create(self, validated_data):
        """create new user profile with encrypted password and return it"""
        return UserProfile.objects.create(**validated_data)
