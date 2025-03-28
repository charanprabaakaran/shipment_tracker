from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.models import User



# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError("Email is required")
        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user
    

    def create_superuser(self, username, email, password):
        user = self.create_user(username, email, password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# class user_table(AbstractBaseUser, PermissionsMixin):
#     username = models.CharField(max_length=150, unique=True, default="default_username")
#     email = models.EmailField(unique=True)
#     phone_number = models.CharField(max_length=15, blank=True, null=True)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
    
#     objects = CustomUserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']

#     def __str__(self):
#         return self.email
    
class Shipment(models.Model):
    STATUS_CHOICES = [
            ('Package Created', 'Package Created'),
            ('Dispatched', 'Dispatched'),
            ('Arrived at Local storage', 'Arrived at Local Storage'),
            ('Out for Delivery', 'Out for Delivery'),
            ('Delivered', 'Delivered'),
            ('Returned', 'Returned'),
        ]

    tracking_number = models.CharField(max_length=50, unique=True)
    destination_address = models.TextField()
    current_status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    estimated_delivery = models.DateField(null=True, blank=True)
    ordered_on = models.DateTimeField(default=timezone.now , blank=True)
    shipped_date = models.DateTimeField(auto_now_add=True ,blank=True)
    delivered_date = models.DateTimeField(null=True, blank=True)
    created_on = models.DateField(null=True, blank=True)
    updated_on = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        # return f"{self.tracking_number} - {self.current_status}"
        return self.tracking_number


class ShipmentStatus(models.Model):
    tracking_number = models.ForeignKey(Shipment, related_name='status_updates', on_delete=models.CASCADE)
    package_status = models.CharField(max_length=50, choices=Shipment.STATUS_CHOICES)
    Comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.tracking_number.tracking_number} - {self.package_status}"