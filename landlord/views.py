from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import LandLord

# Create your views here.
@login_required
def dashboard(request):
    if request.user.position == 'landlord':
        profile = LandLord.objects.get(user = request.user)
    
    context = {
        'profile':profile
    }
    return render(request, 'dashboard/index.html', context)


def tenants(request):
    if request.user.position == 'landlord':
        profile = LandLord.objects.get(user = request.user)
    
    context = {
        'profile':profile
    }
    
    return render(request, 'dashboard/tenants.html', context)




def security(request):
    if request.user.position == 'landlord':
        profile = LandLord.objects.get(user = request.user)
    
    context = {
        'profile':profile
    }
    
    return render(request, 'dashboard/security.html', context)



def invoices(request):

    if request.user.position == 'landlord':
        profile = LandLord.objects.get(user = request.user)
    
    context = {
        'profile':profile
    }
    
    return render(request, 'dashboard/invoices.html', context)
