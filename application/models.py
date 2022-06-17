import datetime
import uuid as uuid
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from twilio.rest import Client


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class UserInfo(AbstractUser):
    username = None
    email = models.EmailField(max_length=50, blank=True, unique=True)
    password = models.CharField(max_length=200, blank=True)
    is_verified = models.BooleanField(default=True)
    first_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20, blank=True)
    mobile_no = models.CharField(blank=True, max_length=10)
    profile = models.ImageField(upload_to='static/user_profile/', default="profile_default.jpeg")
    is_premium = models.BooleanField(max_length=200, blank=True, default=False)
    premium_expiry = models.DateTimeField(blank=True)
    is_partner = models.BooleanField(default=False)
    location = models.CharField(max_length=200, blank=True)
    business_category = (("Cleaner", "Cleaner"), ("Plumber", "Plumber"), ("Teacher", "Teacher"),)
    business_type = models.CharField(choices=business_category, max_length=200, blank=True)
    otp = models.CharField(max_length=200, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'password', 'mobile_no', 'is_partner']
    objects = UserManager()

    def __str__(self):
        return self.email


class UserOTP(models.Model):
    user = models.CharField(max_length=200, blank=True)
    otp = models.CharField(max_length=4, blank=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.user


class paypal_payment(models.Model):
    pay_id = models.CharField(max_length=200, blank=True)
    email = models.EmailField(max_length=200, blank=True)
    amount = models.IntegerField(blank=True)
    currency = models.CharField(max_length=200, blank=True)
    datetime = models.DateTimeField()

    def __str__(self):
        return self.email
