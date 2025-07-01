from django.urls import path
from .views import dashboard, tenants, invoices, security, profile, news, account_settings, estate_pass


urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('tenants/', tenants, name='tenants'),
    path('tenants/<int:tenant_id>/', tenants, name='tenant_detail'),
    path('security/', security, name='security'),
    path('invoices/', invoices, name='invoices'),
    path('profile/', profile, name='profile'),
    path('news/', news, name='news'),
    path('pass/', estate_pass, name='pass'),
    path('settings/', account_settings, name='settings')
]
