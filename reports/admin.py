from django.contrib import admin
from .models import *


class OsagoInline(admin.StackedInline):
    model = Osago
    extra = 0


class VinDecodeInline(admin.StackedInline):
    model = VinDecode
    extra = 0


class PeriodsInline(admin.StackedInline):
    model = VehiclePeriods
    extra = 0


class WantedInline(admin.StackedInline):
    model = Wanted
    extra = 0


class RestrictInline(admin.StackedInline):
    model = Restrict
    extra = 0


class DtpInline(admin.StackedInline):
    model = Dtp
    extra = 0


class DiagnosticActiveInline(admin.StackedInline):
    model = DiagnosticsActive
    extra = 0


class DiagnosticExpiredInline(admin.StackedInline):
    model = DiagnosticsExpired
    extra = 0


class PledgesInline(admin.StackedInline):
    model = Pledges
    extra = 0


class ReviewsInline(admin.StackedInline):
    model = Reviews
    extra = 0


class TaxiInline(admin.StackedInline):
    model = Taxi
    extra = 0


class CustomsInline(admin.StackedInline):
    model = CustomsClearance
    extra = 0


class RNISInline(admin.StackedInline):
    model = RNISRegister
    extra = 0


class ImageInline(admin.StackedInline):
    model = Image
    extra = 0


class VehicleAdmin(admin.ModelAdmin):
    inlines = [
        OsagoInline,
        VinDecodeInline,
        PeriodsInline,
        WantedInline,
        RestrictInline,
        DtpInline,
        DiagnosticActiveInline,
        DiagnosticExpiredInline,
        PledgesInline,
        ReviewsInline,
        TaxiInline,
        CustomsInline,
        RNISInline,
        ImageInline
    ]


admin.site.register(Vehicle, VehicleAdmin)
