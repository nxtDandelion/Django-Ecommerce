from django.db import models
from django.db.models import ForeignKey
from autoslug import AutoSlugField

from apps.accounts.models import User
from apps.common.models import BaseModel


class Seller(BaseModel):
    """
    Seller model

    Attributes:
        General:
            user (ForeignKey): User model
            company_name (CharField): Company name
            slug (AutoSlugField): Slug
            inn_identifier (CharField): Seller INN identifier
            website_url (URLField): Seller's website URL
            phone_number (CharField): Seller phone number
            company_description (CharField): Seller company description

        Company location:
            company_address (CharField): Seller company address
            city (CharField): Seller city
            postal_code (CharField): Seller postal code

        Bank info:
            bank_name (CharField): Seller bank name
            bank_bic_number (CharField): Seller bank bic number
            bank_account_number (CharField): Seller bank account number
    """
    user = ForeignKey(User, on_delete=models.CASCADE, related_name='seller')

    company_name = models.CharField(max_length=120)
    slug = AutoSlugField(populate_from='company_name', always_update=True, null=True, unique=True)
    inn_identifier = models.CharField(max_length=50)
    website_url = models.URLField(null=True, blank=True)
    phone_number = models.CharField(max_length=11)
    company_description = models.TextField()

    company_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)

    bank_name = models.CharField(max_length=120)
    bank_bic_number = models.CharField(max_length=9)
    bank_account_number = models.CharField(max_length=100)

    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.company_name}"
