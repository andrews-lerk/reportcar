from django.contrib import admin
from .models import *


class RecurrentOrderInline(admin.StackedInline):
    model = RecurrentOrder
    extra = 0


class SubscribeAdmin(admin.ModelAdmin):
    inlines = [RecurrentOrderInline, ]


admin.site.register(Subscribe, SubscribeAdmin)
admin.site.register(RateType)
admin.site.register(Order)
admin.site.register(RecurrentOrder)
admin.site.register(PaymentMethod)
