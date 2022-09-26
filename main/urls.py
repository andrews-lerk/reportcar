from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('lk', lk, name='lk'),
    path('login', login_view, name='login'),
    path('auth', auth, name='auth'),
    path('logout', logout_, name='logout'),
    path('check', report_view, name='check'),
    path('report_detail/<str:key>', report_detail, name='report_detail'),
    path('auth-from-restrict', auth_from_restrict, name='auth_restrict')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)