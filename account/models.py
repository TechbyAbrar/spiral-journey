#account/models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .managers import UserManager
from .utils import generate_otp, get_otp_expiry, validate_image

class UserAuth(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['-created_at']
    
    user_id = models.AutoField(primary_key=True)    
    email = models.EmailField(max_length=100, unique=True)
    
    full_name = models.CharField(max_length=30)
    username = models.CharField(max_length=30, unique=True)
    
    profile_pic = models.ImageField(
        upload_to='profile/', 
        default='profile/profile.png',
        null=True,
        blank=True,
        validators=[validate_image]  # Ensure image validation is applied
    )
    
    profile_pic_url = models.URLField(max_length=200, blank=True, null=True)
    
    contanct_no = models.CharField(max_length=15, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)  # Added max_length
    
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_expired = models.DateTimeField(blank=True, null=True)
    
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.full_name

    def set_otp(self, otp=None, expiry_minutes=30):
        self.otp = otp or generate_otp()
        self.otp_expired = get_otp_expiry(expiry_minutes)
        
    def is_otp_valid(self, otp):
        return self.otp == otp and self.otp_expired and timezone.now() <= self.otp_expired