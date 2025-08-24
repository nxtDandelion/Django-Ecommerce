from django.urls import path

from apps.profiles.views import ProfileView, ShippingAddressView, ShippingAddressViewID

urlpatterns = [
    path("", ProfileView.as_view(), name="profile"),
    path("shipping_address/", ShippingAddressView.as_view(), name="shipping_address"),
    path("shipping_addresses/detail/<uuid:id>/", ShippingAddressViewID.as_view(), name="shipping_address_detail"),
]