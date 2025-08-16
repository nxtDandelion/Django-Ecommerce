from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager that leverages Django's auth backend
    """
    def email_validator(self, email):
        try:
            validate_email(email)

        except ValidationError:
            raise ValidationError("Email is not valid")

    def validate_user(self, first_name, last_name, email, password):
        if not first_name or not last_name:
            raise ValueError("Users must have a first and last name")

        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else: ValueError("Email is required")

        if not password:
            raise ValueError("Users must have a password")

    def create_user(self, first_name, last_name, email, password, **extra_fields):
        self.validate_user(first_name, last_name, email, password)

        user = self.model(full_name=first_name, last_name=last_name, email=email, password=password, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def validate_superuser(self, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        return extra_fields

    def create_superuser(self, first_name, last_name, email, password, **extra_fields):
        extra_fields = self.validate_superuser(**extra_fields)
        user = self.create_user(first_name, last_name, email, password, **extra_fields)
        return user