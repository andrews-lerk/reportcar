from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('lk', lk, name='lk'),
    path('login', login_view, name='login'),
    path('auth', auth, name='auth'),
    path('pay-auth', pay_auth, name='pay-auth'),
    path('logout', logout_, name='logout'),
    path('report_detail/<str:key>', report_detail, name='report_detail'),
    path('check', check_car, name='check'),
    path('get-info', get_restrict_data, name='get-info'),
    path('reports', reports_list, name='reports'),
    path('pricing', pricing, name='pricing'),
    path('faq', faq, name='faq'),
    path('politics', politics, name='politics'),
    path('tariffs', tariffs, name='tariffs'),
    path('offer', offer, name='offer')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)