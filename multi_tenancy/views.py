from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from landlord.models import User, LandLord
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def onboarding(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone_number')
        address = request.POST.get('contact_address')
        position = request.POST.get('position')
        
        request.user.position = position
        request.user.save()

        if request.user.position == 'landlord':
            landlord = LandLord(
                user=request.user,
                full_name=full_name,
                phone_number=phone,
                contact_address=address
            )
            landlord.save()
            
            messages.success(request, 'Onboarding completed successfully!')
            return redirect('dashboard')

        else:
            messages.error(request, 'Only landlords can complete onboarding.')
            return redirect('onboarding')


    return render(request, 'auth/onboarding.html')


def index(request):
    return render(request, 'index.html')


def signup(request):
    if request.user.is_anonymous:
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')

            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists.')
                return redirect('signup')

            user = User.objects.create_user(username=username, email=email, password=password)
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            auth_login(request, user)  # Log the user in immediately
            return redirect('onboarding')  # Redirect to onboarding page
    else:
        return redirect('dashboard')
    return render(request, 'auth/register.html')


def login(request):
    if request.user.is_anonymous:
        if request.method == "POST":
            email = request.POST["email"].lower()
            password = request.POST["password"]
            user = authenticate(email=email, password=password)
            if user is not None:
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                auth_login(request, user)
                messages.success(request, "Login successful!")
                return redirect("/")
            else:
                messages.error(request, "Invalid email or password")
                return redirect('login')
    else:
        return redirect("dashboard")
    return render(request, 'auth/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def news(request):
    return render(request, 'dashboard/news.html')