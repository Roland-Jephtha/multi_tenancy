from django.shortcuts import render

# Create your views here.
def dashboard(request):
    return render(request, 'dashboard/index.html')

def tenants(request):
    return render(request, 'dashboard/tenants.html')

def security(request):
    return render(request, 'dashboard/security.html')

def invoices(request):
    return render(request, 'dashboard/invoices.html')
