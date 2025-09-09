from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from apps.common.utils import set_dict_attr
from apps.profiles.models import ShippingAddress
from apps.profiles.serializers import ProfileSerializer, ShippingAddressSerializer

tags = ["Profiles"]

class ProfileView(APIView):
    serializer_class = ProfileSerializer

    @extend_schema(
        summary="Get profile data",
        description="Get data about your profile",
        tags=tags,)
    def get(self, request):
        user = request.user
        serializer = self.serializer_class(user)
        return Response(data=serializer.data, status=200)

    @extend_schema(
        summary="Update profile data",
        description="Update data about your profile",
        tags=tags, )
    def put(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = set_dict_attr(user, serializer.validated_data)
        user.save()
        serializer = self.serializer_class(user)
        return Response(data=serializer.data, status=200)

    @extend_schema(
        summary="Deactivate account",
        description="Deactivate your account",
        tags=tags, )
    def delete(self, request):
        user = request.user
        user.is_active = False
        user.save()
        return Response(data={"message": "User Account Deactivated"})

class ShippingAddressView(APIView):
    serializer_class = ShippingAddressSerializer

    @extend_schema(
        summary="Get shipping address",
        description="Get all shipping addresses associated with your user",
        tags=tags, )
    def get(self, request, *args, **kwargs):
        user = request.user
        shipping_address = ShippingAddress.objects.filter(user=user)
        serializer = self.serializer_class(shipping_address, many=True)
        return Response(data=serializer.data, status=200)

    @extend_schema(
        summary="Create shipping address",
        description="Create shipping address associated with your user",
        tags=tags, )
    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        shipping_address, _ = ShippingAddress.objects.get_or_create(user=user, **data)
        serializer = self.serializer_class(shipping_address)
        return Response(data=serializer.data, status=201)

class ShippingAddressViewID(APIView):
    serializer_class = ShippingAddressSerializer

    def get_object(self, user, shipping_id):
        shipping_address = ShippingAddress.objects.get_or_none(user=user, id=shipping_id)
        return shipping_address

    @extend_schema(
        summary="Get user shipping address",
        description="Get user shipping address by id",
        tags=tags, )
    def get(self, request, *args, **kwargs):
        user = request.user
        shipping_address = self.get_object(user, kwargs["id"])
        if not shipping_address:
            return Response(data={"message": "Shipping Address does not exist!"}, status=404)
        serializer = self.serializer_class(shipping_address)
        return Response(data=serializer.data)

    @extend_schema(
        summary="Update shipping address",
        description="Update shipping address by id",
        tags=tags, )
    def put(self, request, *args, **kwargs):
        user = request.user
        shipping_address = self.get_object(user, kwargs["id"])
        if not shipping_address:
            return Response(data={"message": "Shipping Address does not exist!"}, status=404)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        shipping_address = set_dict_attr(shipping_address, data)
        shipping_address.save()
        serializer = self.serializer_class(shipping_address)
        return Response(data=serializer.data, status=200)

    @extend_schema(
        summary="Delete shipping address",
        description="Delete shipping address by id",
        tags=tags, )
    def delete(self, request, *args, **kwargs):
        user = request.user
        shipping_address = self.get_object(user, kwargs["id"])
        if not shipping_address:
            return Response(data={"message": "Shipping Address does not exist!"}, status=404)
        shipping_address.delete()
        return Response(data={"message": "Shipping address deleted successfully"}, status=200)