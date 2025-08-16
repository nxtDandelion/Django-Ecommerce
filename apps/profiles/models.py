from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

from apps.accounts.models import User
from apps.common.models import BaseModel


class ShippingAddress(BaseModel):
    """
    Shipping address model

    Attributes:
        user (ForeignKey): The user who owns the shipping address
        full_name (CharField): The full name of the recipient
        email (CharField): The email address of the recipient
        phone (CharField): The phone number of the recipient
        address (CharField): The address of the recipient
        city (CharField): The city of the recipient
        country (CharField): The country of the recipient
        zip_code (CharField): The zip code of the recipient

    Methods:
        __str__(self): Returns the string representation of the shipping address
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shipping_addresses')
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=11)
    address = models.CharField(max_length=1000)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=6)

    def __str__(self):
        return f"{self.full_name}'s shipping details"
