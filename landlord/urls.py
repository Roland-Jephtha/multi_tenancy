from django.urls import path
from .views import (
    dashboard, tenants, invoices, security, profile, news, account_settings,
    estate_pass, dependents, add_apartment, add_dependent, edit_dependent, delete_dependent,
    add_security, edit_security, delete_security, toggle_security_approval,
    add_news, edit_news, delete_news, view_notifications
)


urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('tenants/', tenants, name='tenants'),
    path('tenants/<int:tenant_id>/', tenants, name='tenant_detail'),
    path('security/', security, name='security'),
    path('dependents/', dependents, name='dependents'),
    path('invoices/', invoices, name='invoices'),
    path('profile/', profile, name='profile'),
    path('news/', news, name='news'),
    path('pass/', estate_pass, name='pass'),
    path('settings/', account_settings, name='settings'),
    path('add-apartment/', add_apartment, name='add_apartment'),
    path('add-dependent/', add_dependent, name='add_dependent'),
    path('edit-dependent/<int:dependent_id>/', edit_dependent, name='edit_dependent'),
    path('delete-dependent/<int:dependent_id>/', delete_dependent, name='delete_dependent'),
    path('add-security/', add_security, name='add_security'),
    path('edit-security/<int:security_id>/', edit_security, name='edit_security'),
    path('delete-security/<int:security_id>/', delete_security, name='delete_security'),
    path('toggle-security-approval/<int:security_id>/', toggle_security_approval, name='toggle_security_approval'),
    path('add-news/', add_news, name='add_news'),
    path('edit-news/<int:news_id>/', edit_news, name='edit_news'),
    path('delete-news/<int:news_id>/', delete_news, name='delete_news'),
    path('notifications/', view_notifications, name='view_notifications'),
]
