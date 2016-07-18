from django.contrib import admin
from . import models


admin.site.register(models.Batch)
admin.site.register(models.Offer)
admin.site.register(models.CurrencyList)
admin.site.register(models.ExchangeRate)

