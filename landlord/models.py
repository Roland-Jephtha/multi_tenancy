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
    profile_image = models.ImageField(upload_to='profile_image', blank = True, null = True)
    property_status = models.CharField(max_length=100, null = True)
    timestamp = models.DateTimeField(auto_now_add=True, null = True)

    def __str__(self):
        return f"{self.user} - {self.contact_address}"

    def get_profile_completion_percentage(self):
        """Calculate profile completion percentage based on filled fields"""
        # Define the fields that should be considered for profile completion
        required_fields = [
            'title',
            'full_name',
            'phone_number',
            'contact_address',
            'business_office_address_or_position',
            'property_address',
            'year_of_allocation',
            'email',
            'property_status',
            'profile_image'
        ]

        filled_fields = 0
        total_fields = len(required_fields)

        for field in required_fields:
            field_value = getattr(self, field, None)

            # Check if field has a meaningful value
            if field_value is not None:
                if isinstance(field_value, str) and field_value.strip():
                    filled_fields += 1
                elif isinstance(field_value, int) and field_value > 0:
                    filled_fields += 1
                elif hasattr(field_value, 'name'):  # For file fields like profile_image
                    filled_fields += 1
                elif not isinstance(field_value, str):  # For other non-string fields
                    filled_fields += 1

        # Calculate percentage
        percentage = (filled_fields / total_fields) * 100
        return round(percentage)

    def get_missing_fields(self):
        """Get list of missing/empty fields for profile completion"""
        field_labels = {
            'title': 'Title',
            'full_name': 'Full Name',
            'phone_number': 'Phone Number',
            'contact_address': 'Contact Address',
            'business_office_address_or_position': 'Business/Office Address',
            'property_address': 'Property Address',
            'year_of_allocation': 'Year of Allocation',
            'email': 'Email Address',
            'property_status': 'Property Status',
            'profile_image': 'Profile Image'
        }

        missing_fields = []

        for field, label in field_labels.items():
            field_value = getattr(self, field, None)

            # Check if field is empty or None
            if field_value is None:
                missing_fields.append(label)
            elif isinstance(field_value, str) and not field_value.strip():
                missing_fields.append(label)
            elif isinstance(field_value, int) and field_value <= 0:
                missing_fields.append(label)
            elif hasattr(field_value, 'name') and not field_value.name:
                missing_fields.append(label)

        return missing_fields


class Apartment(models.Model):
    PROPERTY_STATUS_CHOICES = [
        ('resident', 'Resident'),
        ('commercial', 'Commercial'),
        ('developing', 'Developing'),
        ('undeveloped', 'Undeveloped'),
    ]

    PROPERTY_TYPE_CHOICES = [
        ('apartment', 'Apartment'),
        ('condo', 'Condo'),
        ('studio', 'Studio'),
        ('loft', 'Loft'),
        ('duplex', 'Duplex'),
    ]

    LEASE_TERM_CHOICES = [
        ('1-year', '1-year'),
        ('month-to-month', 'Month-to-Month'),
        ('6-month', '6-month'),
        ('other', 'Other'),
    ]

    landlord = models.ForeignKey(LandLord, on_delete=models.CASCADE, related_name='apartments')
    property_name = models.CharField(max_length=255)
    address = models.TextField()
    property_status = models.CharField(max_length=20, choices=PROPERTY_STATUS_CHOICES)
    total_floors = models.PositiveIntegerField()
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES)
    total_units = models.PositiveIntegerField()
    special_notes = models.TextField(blank=True, null=True)
    monthly_rent = models.DecimalField(max_digits=12, decimal_places=2)
    security_deposit = models.DecimalField(max_digits=12, decimal_places=2)
    building_picture = models.ImageField(upload_to='apartment_images/', blank=True, null=True)
    lease_term = models.CharField(max_length=20, choices=LEASE_TERM_CHOICES)
    is_occupied = models.BooleanField(default=False, help_text="Whether the apartment is currently occupied")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.property_name} - {self.address}--> {self.landlord}"

    class Meta:
        ordering = ['-created_at']


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

    landlord = models.ForeignKey(LandLord, on_delete=models.CASCADE, related_name='dependents')
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


class Security(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    POSITION_CHOICES = [
        ('security_guard', 'Security Guard'),
        ('patrol_officer', 'Patrol Officer'),
        ('cctv_monitor', 'CCTV Monitor'),
        ('supervisor', 'Security Supervisor'),
        ('other', 'Other'),
    ]

    EMPLOYMENT_TYPE_CHOICES = [
        ('full_time', 'Full-time'),
        ('part_time', 'Part-time'),
        ('contract', 'Contract'),
        ('temporary', 'Temporary'),
    ]

    landlord = models.ForeignKey(LandLord, on_delete=models.CASCADE, related_name='security_personnel')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=20)
    residential_address = models.TextField()
    government_id = models.FileField(upload_to='security_ids/', blank=True, null=True)
    position = models.CharField(max_length=30, choices=POSITION_CHOICES)
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPE_CHOICES)
    joining_date = models.DateField()
    profile_picture = models.ImageField(upload_to='security_photos/', blank=True, null=True)
    is_approved = models.BooleanField(default=False, help_text="Whether the security personnel is approved")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.get_position_display()}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_age(self):
        from datetime import date
        today = date.today()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

    def generate_security_id(self):
        """Generate a unique security ID"""
        return f"EBJAYSEC{self.id:05d}"

    @property
    def status_display(self):
        return "Approved" if self.is_approved else "Pending"

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Security Personnel"


class News(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    CATEGORY_CHOICES = [
        ('general', 'General'),
        ('security', 'Security'),
        ('maintenance', 'Maintenance'),
        ('event', 'Event'),
        ('announcement', 'Announcement'),
        ('emergency', 'Emergency'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    excerpt = models.CharField(max_length=300, help_text="Brief summary of the news")
    author = models.ForeignKey(LandLord, on_delete=models.CASCADE, related_name='news_articles')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='normal')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    is_published = models.BooleanField(default=True)
    featured_image = models.ImageField(upload_to='news_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def priority_badge_class(self):
        """Return Bootstrap badge class based on priority"""
        priority_classes = {
            'low': 'bg-secondary-subtle text-secondary',
            'normal': 'bg-primary-subtle text-primary',
            'high': 'bg-warning-subtle text-warning',
            'urgent': 'bg-danger-subtle text-danger',
        }
        return priority_classes.get(self.priority, 'bg-primary-subtle text-primary')

    @property
    def priority_display_text(self):
        """Return display text for priority"""
        priority_text = {
            'low': 'Low',
            'normal': 'New',
            'high': 'Important',
            'urgent': 'Urgent',
        }
        return priority_text.get(self.priority, 'New')

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "News Articles"


class BoardNotification(models.Model):
    NOTIFICATION_TYPE_CHOICES = [
        ('complaint', 'Complaint'),
        ('security_alert', 'Security Alert'),
        ('help_request', 'Help Request'),
        ('suggestion', 'Suggestion'),
        ('maintenance_request', 'Maintenance Request'),
        ('general', 'General'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]

    sender = models.ForeignKey(LandLord, on_delete=models.CASCADE, related_name='board_notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES, default='general')
    subject = models.CharField(max_length=200, blank=True, null=True)
    message = models.TextField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    is_read = models.BooleanField(default=False)
    admin_response = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sender.full_name} - {self.get_notification_type_display()}"

    @property
    def status_badge_class(self):
        """Return Bootstrap badge class based on status"""
        status_classes = {
            'pending': 'bg-warning-subtle text-warning',
            'in_progress': 'bg-info-subtle text-info',
            'resolved': 'bg-success-subtle text-success',
            'closed': 'bg-secondary-subtle text-secondary',
        }
        return status_classes.get(self.status, 'bg-warning-subtle text-warning')

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Board Notifications"