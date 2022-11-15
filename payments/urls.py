from django.urls import path
from .views import *

urlpatterns = [
    path('on-one-time-complete-callback', on_one_time_complete_callback, name='one-time-callback'),
    path('on-recurrent-complete-callback', on_recurrent_complete_callback, name='recurrent-callback')
]