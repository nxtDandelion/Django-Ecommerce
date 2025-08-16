from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

from apps.accounts.managers import CustomUserManager
from apps.common.models import IsDeletedModel

ACCOUNT_TYPE_CHOICES = (
("SELLER", "SELLER"),
("BUYER", "BUYER"),
)


class User(AbstractBaseUser, IsDeletedModel):
    """
    Custom user model that extends AbstractBaseUser.

    Attributes:
        email (EmailField): Email address of the user.
        first_name (str): the first name of the user.
        last_name (str): the last name of the user.
        avatar (ImageField): the avatar of the user.

    """
    email = models.EmailField(verbose_name='Email Address', unique=True)
    first_name = models.CharField(verbose_name='First Name', max_length=50)
    last_name = models.CharField(verbose_name='Last Name', max_length=50)
    avatar = models.ImageField(verbose_name='Avatar', upload_to='avatars/', null=True, blank=True, default='avatars/default.png')

    is_staff = models.BooleanField(verbose_name='Is Admin', default=False)
    is_active = models.BooleanField(verbose_name='Is Active', default=True)

    account_type = models.CharField(verbose_name='Account Type', max_length=6, choices=ACCOUNT_TYPE_CHOICES, default='BUYER')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    @property
    def full_name(self):
        """
        Returns the full name of the user.
        """
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        """
        Returns the string representation of the user.
        """
        return self.full_name

    def has_perm(self, perm, obj=None):
        """
        Returns True if the user has the given permission.
        """
        return True

    def has_module_perms(self, app_label):
        """
        Returns True if the user has the given permission.
        """
        return True

    @property
    def is_superuser(self):
        """
        Returns True if the user is a superuser.
        """
        return self.is_staff