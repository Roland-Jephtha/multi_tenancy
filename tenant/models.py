from django.db import models
from landlord.models import User

# Create your models here.



class Tenant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='tenant_profile', null = True)
    title = models.CharField(max_length=50, null = True)
    full_name = models.CharField(max_length=255, null = True)
    phone_number = models.CharField(max_length=20, null = True)
    contact_address = models.TextField(null = True)
    date_of_tenancy = models.DateField(null = True)
    email = models.EmailField(null = True)
    profile_image = models.ImageField(upload_to='profile_image', blank = True, null = True)
    timestamp = models.DateTimeField(auto_now_add=True, null = True)

    def __str__(self):
        return f"{self.user} - {self.contact_address}"