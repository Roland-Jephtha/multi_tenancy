from django.db import models
from landlord.models import User, Apartment


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
    property_occupied = models.ForeignKey(Apartment, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, null = True)

    def __str__(self):
        return f"{self.user} - {self.contact_address}"
    





class Dependent(models.Model):
    RELATIONSHIP_CHOICES = [
        ('spouse', 'Spouse'),
        ('child', 'Child'),
        ('parent', 'Parent'),
        ('sibling', 'Sibling'),
        ('other', 'Other'),
    ]

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    ID_TYPE_CHOICES = [
        ('national_id', 'National ID'),
        ('voters_card', "Voter's Card"),
        ('drivers_license', "Driver's License"),
        ('international_passport', 'International Passport'),
        ('other', 'Other'),
    ]

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='dependents')
    full_name = models.CharField(max_length=255)
    relationship = models.CharField(max_length=20, choices=RELATIONSHIP_CHOICES)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    passport_photo = models.ImageField(upload_to='dependent_photos/', blank=True, null=True)
    id_type = models.CharField(max_length=30, choices=ID_TYPE_CHOICES)
    id_number = models.CharField(max_length=50)
    medical_notes = models.TextField(blank=True, null=True, help_text="Allergies, disabilities, etc.")
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} ({self.relationship})"

    def get_age(self):
        from datetime import date
        today = date.today()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

    def generate_dependent_id(self):
        """Generate a unique dependent ID"""
        return f"EBJAYSEC{self.id:05d}"

    class Meta:
        ordering = ['-created_at']