from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.loader import render_to_string
from django.http import JsonResponse
from .models import Tenant, Dependent
from landlord.models import Apartment





# Create your views here.
@login_required
def dashboard(request):
    profile = None
    apartments = Apartment.objects.filter(is_occupied=False)
    if request.user.position == 'tenant':
        try:
            profile = Tenant.objects.get(user=request.user)
        except Tenant.DoesNotExist:
            profile = None
    
    if request.method == 'POST' and 'apartment_id' in request.POST and profile:
        apartment_id = request.POST.get('apartment_id')
        apartment = get_object_or_404(Apartment, id=apartment_id)
        profile.property_occupied = apartment
        profile.save()
        messages.success(request, f"Apartment '{apartment.property_name}' selected successfully!")
        return redirect('tenant-dashboard')
    
    context = {
        'profile': profile,
        'apartments': apartments,
    }
    return render(request, 'dashboard/tenant_dashboard.html', context)






def dependents(request):
    if request.user.position == 'tenant':
        profile = Tenant.objects.get(user = request.user)
        dependents_list = Dependent.objects.filter(tenant=profile)

    context = {
        'profile': profile,
        'dependents': dependents_list,
    }

    return render(request, 'dashboard/dependants.html', context)







