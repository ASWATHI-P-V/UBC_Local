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
