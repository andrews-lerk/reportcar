from django.contrib import admin
from django import forms

from .models import FAQ, ReportsViewCounter
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class FAQForm(forms.ModelForm):
    answer = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = FAQ
        fields = '__all__'


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    form = FAQForm


admin.site.register(ReportsViewCounter)
