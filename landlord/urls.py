from django.urls import path
from .views import dashboard, tenants, invoices, security, profile


urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('tenants/', tenants, name='tenants'),
    path('tenants/<int:tenant_id>/', tenants, name='tenant_detail'),
    path('security/', security, name='security'),
    path('invoices/', invoices, name='invoices'),
    path('profile/', profile, name='profile'),
]
