from rest_framework import serializers
from apps.accounts.models import User
from apps.profiles.models import ShippingAddress


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'avatar', 'account_type']
        read_only_fields = ['email', 'account_type']
        extra_kwargs = {'avatar': {'required': False}}

class ShippingAddressSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    full_name = serializers.CharField(max_length=500)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=12)
    address = serializers.CharField(max_length=1000)
    city = serializers.CharField(max_length=100)
    country = serializers.CharField()
    zip_code = serializers.CharField()