from django.contrib import admin

# Register your models here.
# agents/admin.py
from django.contrib import admin
from .models import cryptcurrencyratemodel, CurrencyUpdateModel
admin.site.register(cryptcurrencyratemodel)
admin.site.register(CurrencyUpdateModel)
 # This is fine