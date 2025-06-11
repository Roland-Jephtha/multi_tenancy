from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.

class User(AbstractUser):

    POSITION_CHOICES = [
        ("landlord", "Landlord"),
        ("tenant", "Tenant"),

    ]
    email = models.EmailField(unique=True, null=True)
    username =  models.CharField(max_length=15, blank=True, null=True)


    position = models.CharField(
        max_length=20,
        choices=POSITION_CHOICES,
        blank=True,  # allow blank
        null=True,   # allow null
        help_text=_("Individual's position in the system (e.g., Landlord, Tenant)."),
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']



    def __str__(self):
        return f"{self.username}"



class LandLord(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='landlord_profile', null = True)
    title = models.CharField(max_length=50, null = True)
    full_name = models.CharField(max_length=255, null = True)
    phone_number = models.CharField(max_length=20, null = True)
    contact_address = models.TextField(null = True)
    business_office_address_or_position = models.TextField(null = True)
    property_address = models.CharField(max_length=100, help_text="Write Your Plot Number in Full (e.g., Plot S8-C)", null = True)
    year_of_allocation = models.PositiveIntegerField(null = True)
    email = models.EmailField(null = True)
    property_status = models.CharField(max_length=100, null = True)
    timestamp = models.DateTimeField(auto_now_add=True, null = True)

    def __str__(self):
        return f"{self.user} - {self.contact_address}"