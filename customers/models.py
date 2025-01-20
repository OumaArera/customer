from django.db import models # type: ignore
from django.utils.translation import gettext_lazy as gtl # type: ignore
from phonenumber_field.modelfields import PhoneNumberField # type: ignore


class Customer(models.Model):
    """
    Custom Customer model that includes additional fields.
    """
    customer_id = models.AutoField(primary_key=True)
    phone_number = PhoneNumberField(
        unique=True,
        error_messages={"unique": gtl("A customer with the provided phone number already exists")},
        help_text=gtl("Enter a valid phone number"),
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(
        null=True,
        blank=True,
        unique=True,
        error_messages={"unique": gtl("A user with that email already exists.")},
    )
    customer_code = models.CharField(
        max_length=100,
        unique=True,
        error_messages={"unique": gtl("A customer with the provided code already exists")},
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        if self.email == "":
            self.email = None
        super().save(*args, **kwargs)

    @classmethod
    def create_customer(cls, validated_data):
        """Creates a new customer instance from the validated data."""

        customer = cls(**validated_data)
        return customer
