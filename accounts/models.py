from django.db import models
from django.utils import timezone

class User(models.Model):
    name = models.CharField(max_length=100,null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone = models.CharField(max_length=20, unique=True)  # Supports country code
    is_whatsapp = models.BooleanField(default=False)
    country_code = models.CharField(max_length=5, null=True, blank=True)

    # OTP fields
    otp = models.CharField(max_length=6, unique=True, null=True, blank=True)
    otp_created_at = models.DateTimeField(null=True, blank=True)

    def is_otp_valid(self, otp_input, expiry_seconds=300):
        if self.otp != otp_input or not self.otp_created_at:
            return False
        return (timezone.now() - self.otp_created_at).total_seconds() <= expiry_seconds

    def __str__(self):
        return f"{self.phone} - {self.name or 'Unregistered'}"


# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# class User(AbstractBaseUser, PermissionsMixin):
#     # --- Core fields ---
#     email = models.EmailField(unique=True)
#     full_name = models.CharField(max_length=255)
#     phone_number = models.CharField(max_length=20, unique=True)
#     address = models.TextField(blank=True, null=True)

#     # --- Profile-related fields ---
#     ROLE_CHOICES = (
#         ('individual', 'Individual'),
#         ('business', 'Business'),
#     )
#     role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='individual')
#     profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
#     category = models.CharField(max_length=100, blank=True, null=True)
#     designation = models.CharField(max_length=100, blank=True, null=True)
#     about = models.TextField(blank=True, null=True)
#     enable_destination_and_company_name = models.BooleanField(default=False)

#     # --- Business-specific fields ---
#     business_name = models.CharField(max_length=255, blank=True, null=True)
#     company_name = models.CharField(max_length=255, blank=True, null=True)
#     logo = models.ImageField(upload_to='logos/', blank=True, null=True)

#     # --- Admin fields ---
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)

#     # --- Manager & Auth ---
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['full_name']

#     def __str__(self):
#         return self.email
