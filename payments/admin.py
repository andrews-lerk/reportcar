from django.contrib import admin
from .models import *

admin.site.register(OneTimePayment)
admin.site.register(RateType)
admin.site.register(SubscribePaymentMethod)
admin.site.register(SubscribePayment)
admin.site.register(RateSubscribe)