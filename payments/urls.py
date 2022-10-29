from django.urls import path
from .views import *

urlpatterns = [
    path('pay-callback', pay_callback, name='pay-callback'),
    path('pay-redirect', pay_redirect, name='pay-redirect')
]