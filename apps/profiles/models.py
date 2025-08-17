from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.db.models.fields.related import ForeignKey

from apps.accounts.models import User
from apps.common.models import BaseModel
from apps.common.utils import generate_unique_code
from apps.shop.models import Product


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


DELIVERY_STATUS_CHOICES = (
    ("PENDING", "PENDING"),
    ("PACKING", "PACKING"),
    ("SHIPPING", "SHIPPING"),
    ("ARRIVING", "ARRIVING"),
    ("SUCCESS", "SUCCESS"),
)

PAYMENT_STATUS_CHOICES = (
    ("PENDING", "PENDING"),
    ("PROCESSING", "PROCESSING"),
    ("SUCCESS", "SUCCESS"),
    ("CANCELLED", "CANCELLED"),
    ("FAILED", "FAILED"),
)


class Order(BaseModel):
    """
    Order model

    Attributes:
        user (ForeignKey): The user who owns the order
        transaction_id (CharField): The transaction id of the order
        delivery_status (CharField): The delivery status of the order
        payment_status (CharField): The payment status of the order
        date_delivered (DateTimeField): The date the order was delivered

        full_name (CharField): The full name of the buyer
        email (CharField): The email address of the buyer
        phone_number (CharField): The phone number of the buyer
        address (CharField): The address of the buyer
        city (CharField): The city of the buyer
        country (CharField): The country of the buyer
        zip_code (CharField): The zip code of the buyer
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    transaction_id = models.CharField(max_length=100, unique=True, blank=True)
    delivery_status = models.CharField(max_length=20, choices=DELIVERY_STATUS_CHOICES, default='PENDING')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='PENDING')
    date_delivered = models.DateTimeField(null=True, blank=True)

    full_name = models.CharField(max_length=100, null=True)
    email = models.EmailField(null=True)
    phone_number = models.CharField(max_length=11, null=True)
    address = models.CharField(max_length=1100, null=True)
    city = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100, null=True)
    zip_code = models.CharField(max_length=6, null=True)

    def __str__(self):
        return f"{self.full_name}'s order"

    def save(self, *args, **kwargs) -> None:
        if not self.created_at:
            self.transaction_id = generate_unique_code(Order, "transaction_id")
        super().save(*args, **kwargs)


class OrderItem(BaseModel):
    """
    Represents an order item

    Attributes:
        user (ForeignKey): The user who owns the orders
        order (ForeignKey): The order to which the item was added
        product (ForeignKey): The product of the order
        quantity (IntegerField): The quantity of the product ordered by the user
    """
    user = ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    order = ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True, related_name='items')
    product = ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, related_name='items')
    quantity = models.PositiveIntegerField(default=1)

    @property
    def get_total_price(self):
        return self.product.price_current * self.quantity

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.product.name