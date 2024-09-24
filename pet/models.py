from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.conf import settings
import secrets

from django.contrib.auth.models import AbstractUser
from django.db import models



class wallet(models.Model):
    balance = models.DecimalField(max_digits=10, decimal_places=2)


    


class Donation(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    country = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    city = models.CharField(max_length=255)
    message = models.TextField()



class SignUp(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=300)



class OtpToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="otps")
    otp_code = models.CharField(max_length=6, default=secrets.token_hex(3))
    tp_created_at = models.DateTimeField(auto_now_add=True)
    otp_expires_at = models.DateTimeField(blank=True, null=True)
    
    
    def __str__(self):
        return self.user.username