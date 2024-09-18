from django.contrib import admin

# Register your models here.
from .models import Donation, wallet

admin.site.register(Donation)
admin.site.register(wallet)
