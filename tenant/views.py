from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.loader import render_to_string
from django.http import JsonResponse
from .models import Tenant, Dependent

# Create your views here.
@login_required
def dashboard(request):
    # if request.user.position == 'tenant':
    #     profile = Tenant.objects.get(user = request.user)
    
    # context = {
    #     'profile':profile
    # }
    
    return render(request, 'dashboard/tenant_dashboard.html')







def dependents(request):
    if request.user.position == 'tenant':
        profile = Tenant.objects.get(user = request.user)
        dependents_list = Dependent.objects.filter(tenant=profile)

    context = {
        'profile': profile,
        'dependents': dependents_list,
    }

    return render(request, 'dashboard/dependants.html', context)







