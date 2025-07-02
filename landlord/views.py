from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.loader import render_to_string
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


def profile(request):
    if request.user.position == 'landlord':
        profile = LandLord.objects.get(user=request.user)
        
        if request.method == 'POST':
            # Update user fields
            request.user.email = request.POST.get('email')
            request.user.save()
            
            # Update profile fields
            profile.title = request.POST.get('title')
            profile.full_name = request.POST.get('full_name')
            profile.phone_number = request.POST.get('phone_number')
            profile.contact_address = request.POST.get('contact_address')
            profile.business_office_address_or_position = request.POST.get('business_office_address_or_position')
            profile.property_address = request.POST.get('property_address')
            profile.year_of_allocation = request.POST.get('year_of_allocation')
            profile.property_status = request.POST.get('property_status')
            
            # Handle profile image if uploaded
            if request.FILES.get('profile_image'):
                profile.profile_image = request.FILES['profile_image']
            
            profile.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    
    context = {
        'profile': profile
    }
    
    return render(request, 'dashboard/profile.html', context)


def news(request):
    if request.user.position == 'landlord':
        profile = LandLord.objects.get(user = request.user)
    
    context = {
        'profile':profile
    }
    
    return render(request, 'dashboard/news.html', context)



def account_settings(request):
    if request.user.position == 'landlord':
        profile = LandLord.objects.get(user = request.user)
    
    context = {
        'profile':profile
    }
    
    return render(request, 'dashboard/settings.html', context)


def estate_pass(request):
    if request.user.position == 'landlord':
        profile = LandLord.objects.get(user = request.user)
    
    context = {
        'profile':profile
    }
    
    return render(request, 'dashboard/estate-pass.html', context)


def dependents(request):
    if request.user.position == 'landlord':
        profile = LandLord.objects.get(user = request.user)
    
    context = {
        'profile':profile
    }
    
    return render(request, 'dashboard/dependants.html', context)
