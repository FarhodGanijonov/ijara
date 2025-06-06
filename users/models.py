from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, phone, full_name, password=None, **extra_fields):
        if not phone:
            raise ValueError('The Phone field must be set')
        if not full_name:
            raise ValueError('The Full Name field must be set')

        extra_fields.setdefault('is_active', True)

        user = self.model(phone=phone, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, full_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone, full_name, password, **extra_fields)


class AbstractUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('Seller', 'Sotuvchi'),
        ('Buyer', 'Xaridor'),
    ]

    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, unique=True)
    passport_scan = models.ImageField(upload_to='passport_scan/', blank=True, null=True)
    passport_back_scan = models.ImageField(upload_to='passport_back_scan', blank=True, null=True)
    passport_scan_with_face = models.ImageField(upload_to='passport_scan_with_face', blank=True, null=True)
    passport_seria = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    #  Django admin ishlashi uchun majburiy maydonlar:
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return f"{self.full_name} | {self.phone}"
