from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
# from .models import wallet

class wallet(models.Model):
    # user = models.OneToOneField( on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    # email = models.EmailField(unique=True)
    # first_name = models.CharField(max_length=255)
    # last_name = models.CharField(max_length=255)

    # USERNAME_FIELD = 'dav@k.com'
    # REQUIRED_FIELDS = ['first_name', 'last_name']

    


class Donation(models.Model):
    # user = models.ForeignKey(wallet, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    country = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    city = models.CharField(max_length=255)
    message = models.TextField()
