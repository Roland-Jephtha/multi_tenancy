from django.urls import path
from .views import dashboard, dependents


urlpatterns = [
    path('', dashboard, name='tenant-dashboard'),
    path('dependents/', dependents, name='tenant-dependents'),

]