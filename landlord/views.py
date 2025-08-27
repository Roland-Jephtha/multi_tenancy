from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.loader import render_to_string
from django.http import JsonResponse
from .models import LandLord, Apartment, Dependent, Security, News, BoardNotification
from tenant.models import Tenant, Dependent as TenantDependent

# Create your views here.
@login_required
def dashboard(request):
    if request.user.position == 'landlord':
        profile = LandLord.objects.get(user = request.user)

        # Get apartment statistics
        apartments = Apartment.objects.filter(landlord=profile)
        total_apartments = apartments.count()
        occupied_apartments = apartments.filter(is_occupied=True).count()
        vacant_apartments = apartments.filter(is_occupied=False).count()

        # Get recent apartments (last 5)
        recent_apartments = apartments.order_by('-created_at')[:5]

        # Get profile completion data
        profile_completion_percentage = profile.get_profile_completion_percentage()
        missing_fields = profile.get_missing_fields()

    context = {
        'profile': profile,
        'total_apartments': total_apartments,
        'occupied_apartments': occupied_apartments,
        'vacant_apartments': vacant_apartments,
        'recent_apartments': recent_apartments,
        'apartments': apartments,
        'profile_completion_percentage': profile_completion_percentage,
        'missing_fields': missing_fields,
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
        security_personnel = Security.objects.filter(landlord=profile)
        approved_count = security_personnel.filter(is_approved=True).count()
        pending_count = security_personnel.filter(is_approved=False).count()

    context = {
        'profile': profile,
        'security_personnel': security_personnel,
        'approved_count': approved_count,
        'pending_count': pending_count,
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
    

    

    elif request.user.position == 'tenant':
        profile = Tenant.objects.get(user=request.user)
        
        if request.method == 'POST':
            # Update user fields
            request.user.email = request.POST.get('email')
            request.user.save()
            
            # Update profile fields
            profile.title = request.POST.get('title')
            profile.full_name = request.POST.get('full_name')
            profile.phone_number = request.POST.get('phone_number')
            profile.contact_address = request.POST.get('contact_address')
            profile.property_occupied = request.POST.get('property_occupied')
            profile.date_of_tenancy = request.POST.get('date_of_tenancy')
            
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

        # Handle board notification submission
        if request.method == 'POST':
            message = request.POST.get('message')
            notification_type = request.POST.get('notification_type', 'general')
            subject = request.POST.get('subject', '')

            if message:
                BoardNotification.objects.create(
                    sender=profile,
                    notification_type=notification_type,
                    subject=subject,
                    message=message
                )
                messages.success(request, 'Your message has been sent to the Estate Board!')
            else:
                messages.error(request, 'Please enter a message.')

            return redirect('news')

        # Get latest news articles (limit to 5 for the main page)
        latest_news = News.objects.filter(is_published=True)[:5]

        # Get user's notifications status
        user_notifications = BoardNotification.objects.filter(sender=profile)[:3]

    context = {
        'profile': profile,
        'latest_news': latest_news,
        'user_notifications': user_notifications,
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
        dependents_list = Dependent.objects.filter(landlord=profile)

 
    elif request.user.position == 'tenant':
        profile = Tenant.objects.get(user = request.user)
        dependents_list = TenantDependent.objects.filter(tenant=profile)
        

    context = {
        'profile': profile,
        'dependents': dependents_list,
    }

    return render(request, 'dashboard/estate-pass.html', context)


def dependents(request):
    if request.user.position == 'landlord':
        profile = LandLord.objects.get(user = request.user)
        dependents_list = Dependent.objects.filter(landlord=profile)

    elif request.user.position == 'tenant':
        profile = Tenant.objects.get(user = request.user)
        dependents_list = Dependent.objects.filter(tenant=profile)

    context = {
        'profile': profile,
        'dependents': dependents_list,
    }

    return render(request, 'dashboard/dependants.html', context)


@login_required
def add_apartment(request):
    if request.user.position != 'landlord':
        messages.error(request, 'Only landlords can add apartments.')
        return redirect('dashboard')

    if request.method == 'POST':
        try:
            # Get the landlord profile
            landlord_profile = LandLord.objects.get(user=request.user)

            # Create new apartment
            apartment = Apartment(
                landlord=landlord_profile,
                property_name=request.POST.get('property_name'),
                address=request.POST.get('address'),
                property_status=request.POST.get('property_status'),
                total_floors=request.POST.get('total_floors'),
                property_type=request.POST.get('property_type'),
                total_units=request.POST.get('total_units'),
                special_notes=request.POST.get('special_notes', ''),
                monthly_rent=request.POST.get('monthly_rent'),
                security_deposit=request.POST.get('security_deposit'),
                lease_term=request.POST.get('lease_term'),
            )

            # Handle file upload if provided
            if request.FILES.get('building_picture'):
                apartment.building_picture = request.FILES['building_picture']

            apartment.save()
            messages.success(request, 'Apartment added successfully!')

        except LandLord.DoesNotExist:
            messages.error(request, 'Landlord profile not found. Please complete your profile first.')
        except Exception as e:
            messages.error(request, f'Error adding apartment: {str(e)}')

    return redirect('dashboard')


@login_required
def add_dependent(request):
    if request.user.position == 'landlord':


        if request.method == 'POST':
            try:
                # Get the landlord profile
                landlord_profile = LandLord.objects.get(user=request.user)

                # Create new dependent
                dependent = Dependent(
                    landlord=landlord_profile,
                    full_name=request.POST.get('full_name'),
                    relationship=request.POST.get('relationship'),
                    date_of_birth=request.POST.get('date_of_birth'),
                    gender=request.POST.get('gender'),
                    phone_number=request.POST.get('phone_number', ''),
                    email=request.POST.get('email', ''),
                    id_type=request.POST.get('id_type'),
                    id_number=request.POST.get('id_number'),
                    medical_notes=request.POST.get('medical_notes', ''),
                    remarks=request.POST.get('remarks', ''),
                )

                # Handle file upload if provided
                if request.FILES.get('passport_photo'):
                    dependent.passport_photo = request.FILES['passport_photo']

                dependent.save()
                messages.success(request, 'Dependent added successfully!')

            except LandLord.DoesNotExist:
                messages.error(request, 'Landlord profile not found. Please complete your profile first.')
            except Exception as e:
                messages.error(request, f'Error adding dependent: {str(e)}')
        return redirect('tenant-dependents')




    elif request.user.position == 'tenant':

        if request.method == 'POST':
            try:
                # Get the landlord profile
                tenant_profile = Tenant.objects.get(user=request.user)

                # Create new dependent
                dependent = TenantDependent(
                    tenant=tenant_profile,
                    full_name=request.POST.get('full_name'),
                    relationship=request.POST.get('relationship'),
                    date_of_birth=request.POST.get('date_of_birth'),
                    gender=request.POST.get('gender'),
                    phone_number=request.POST.get('phone_number', ''),
                    email=request.POST.get('email', ''),
                    id_type=request.POST.get('id_type'),
                    id_number=request.POST.get('id_number'),
                    medical_notes=request.POST.get('medical_notes', ''),
                    remarks=request.POST.get('remarks', ''),
                )

                # Handle file upload if provided
                if request.FILES.get('passport_photo'):
                    dependent.passport_photo = request.FILES['passport_photo']

                dependent.save()
                messages.success(request, 'Dependent added successfully!')

            except LandLord.DoesNotExist:
                messages.error(request, 'Landlord profile not found. Please complete your profile first.')
            except Exception as e:
                messages.error(request, f'Error adding dependent: {str(e)}')

    

        return redirect('tenant-dependents')


@login_required
def edit_dependent(request, dependent_id):
    if request.user.position == 'landlord':
 

        try:
            landlord_profile = LandLord.objects.get(user=request.user)
            dependent = get_object_or_404(Dependent, id=dependent_id, landlord=landlord_profile)

            if request.method == 'POST':
                # Update dependent fields
                dependent.full_name = request.POST.get('full_name')
                dependent.relationship = request.POST.get('relationship')
                dependent.date_of_birth = request.POST.get('date_of_birth')
                dependent.gender = request.POST.get('gender')
                dependent.phone_number = request.POST.get('phone_number', '')
                dependent.email = request.POST.get('email', '')
                dependent.id_type = request.POST.get('id_type')
                dependent.id_number = request.POST.get('id_number')
                dependent.medical_notes = request.POST.get('medical_notes', '')
                dependent.remarks = request.POST.get('remarks', '')

                # Handle file upload if provided
                if request.FILES.get('passport_photo'):
                    dependent.passport_photo = request.FILES['passport_photo']

                dependent.save()
                messages.success(request, 'Dependent updated successfully!')
                return redirect('dependents')

        except LandLord.DoesNotExist:
            messages.error(request, 'Landlord profile not found.')
        except Exception as e:
            messages.error(request, f'Error updating dependent: {str(e)}')

        return redirect('dependents')
    

    elif request.user.position == 'tenant':
 

        try:
            tenant_profile = Tenant.objects.get(user=request.user)
            dependent = get_object_or_404(TenantDependent, id=dependent_id, tenant=tenant_profile)

            if request.method == 'POST':
                # Update dependent fields
                dependent.full_name = request.POST.get('full_name')
                dependent.relationship = request.POST.get('relationship')
                dependent.date_of_birth = request.POST.get('date_of_birth')
                dependent.gender = request.POST.get('gender')
                dependent.phone_number = request.POST.get('phone_number', '')
                dependent.email = request.POST.get('email', '')
                dependent.id_type = request.POST.get('id_type')
                dependent.id_number = request.POST.get('id_number')
                dependent.medical_notes = request.POST.get('medical_notes', '')
                dependent.remarks = request.POST.get('remarks', '')

                # Handle file upload if provided
                if request.FILES.get('passport_photo'):
                    dependent.passport_photo = request.FILES['passport_photo']

                dependent.save()
                messages.success(request, 'Dependent updated successfully!')
                return redirect('dependents')

        except Tenant.DoesNotExist:
            messages.error(request, 'Tenant profile not found.')
        except Exception as e:
            messages.error(request, f'Error updating dependent: {str(e)}')

        return redirect('tenant-dependents')


@login_required
def delete_dependent(request, dependent_id):
    if request.user.position != 'landlord':
        messages.error(request, 'Only landlords can delete dependents.')
        return redirect('dependents')

    try:
        landlord_profile = LandLord.objects.get(user=request.user)
        dependent = get_object_or_404(Dependent, id=dependent_id, landlord=landlord_profile)

        if request.method == 'POST':
            dependent_name = dependent.full_name
            dependent.delete()
            messages.success(request, f'Dependent "{dependent_name}" deleted successfully!')
        else:
            messages.error(request, 'Invalid request method.')

    except LandLord.DoesNotExist:
        messages.error(request, 'Landlord profile not found.')
    except Exception as e:
        messages.error(request, f'Error deleting dependent: {str(e)}')

    return redirect('dependents')


@login_required
def add_security(request):
    if request.user.position != 'landlord':
        messages.error(request, 'Only landlords can add security personnel.')
        return redirect('security')

    if request.method == 'POST':
        try:
            # Get the landlord profile
            landlord_profile = LandLord.objects.get(user=request.user)

            # Create new security personnel
            security_person = Security(
                landlord=landlord_profile,
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                gender=request.POST.get('gender'),
                date_of_birth=request.POST.get('date_of_birth'),
                phone_number=request.POST.get('phone_number'),
                residential_address=request.POST.get('residential_address'),
                position=request.POST.get('position'),
                employment_type=request.POST.get('employment_type'),
                joining_date=request.POST.get('joining_date'),
                is_approved=False,  # Default to pending approval
            )

            # Handle file uploads if provided
            if request.FILES.get('government_id'):
                security_person.government_id = request.FILES['government_id']
            if request.FILES.get('profile_picture'):
                security_person.profile_picture = request.FILES['profile_picture']

            security_person.save()
            messages.success(request, 'Security personnel added successfully! Pending approval.')

        except LandLord.DoesNotExist:
            messages.error(request, 'Landlord profile not found. Please complete your profile first.')
        except Exception as e:
            messages.error(request, f'Error adding security personnel: {str(e)}')

    return redirect('security')


@login_required
def edit_security(request, security_id):
    if request.user.position != 'landlord':
        messages.error(request, 'Only landlords can edit security personnel.')
        return redirect('security')

    try:
        landlord_profile = LandLord.objects.get(user=request.user)
        security_person = get_object_or_404(Security, id=security_id, landlord=landlord_profile)

        if request.method == 'POST':
            # Update security personnel fields
            security_person.first_name = request.POST.get('first_name')
            security_person.last_name = request.POST.get('last_name')
            security_person.gender = request.POST.get('gender')
            security_person.date_of_birth = request.POST.get('date_of_birth')
            security_person.phone_number = request.POST.get('phone_number')
            security_person.residential_address = request.POST.get('residential_address')
            security_person.position = request.POST.get('position')
            security_person.employment_type = request.POST.get('employment_type')
            security_person.joining_date = request.POST.get('joining_date')

            # Handle file uploads if provided
            if request.FILES.get('government_id'):
                security_person.government_id = request.FILES['government_id']
            if request.FILES.get('profile_picture'):
                security_person.profile_picture = request.FILES['profile_picture']

            security_person.save()
            messages.success(request, 'Security personnel updated successfully!')
            return redirect('security')

    except LandLord.DoesNotExist:
        messages.error(request, 'Landlord profile not found.')
    except Exception as e:
        messages.error(request, f'Error updating security personnel: {str(e)}')

    return redirect('security')


@login_required
def delete_security(request, security_id):
    if request.user.position != 'landlord':
        messages.error(request, 'Only landlords can delete security personnel.')
        return redirect('security')

    try:
        landlord_profile = LandLord.objects.get(user=request.user)
        security_person = get_object_or_404(Security, id=security_id, landlord=landlord_profile)

        if request.method == 'POST':
            security_name = security_person.full_name
            security_person.delete()
            messages.success(request, f'Security personnel "{security_name}" deleted successfully!')
        else:
            messages.error(request, 'Invalid request method.')

    except LandLord.DoesNotExist:
        messages.error(request, 'Landlord profile not found.')
    except Exception as e:
        messages.error(request, f'Error deleting security personnel: {str(e)}')

    return redirect('security')


@login_required
def toggle_security_approval(request, security_id):
    if request.user.position != 'landlord':
        messages.error(request, 'Only landlords can approve security personnel.')
        return redirect('security')

    try:
        landlord_profile = LandLord.objects.get(user=request.user)
        security_person = get_object_or_404(Security, id=security_id, landlord=landlord_profile)

        if request.method == 'POST':
            security_person.is_approved = not security_person.is_approved
            security_person.save()

            status = "approved" if security_person.is_approved else "pending"
            messages.success(request, f'Security personnel "{security_person.full_name}" status changed to {status}!')
        else:
            messages.error(request, 'Invalid request method.')

    except LandLord.DoesNotExist:
        messages.error(request, 'Landlord profile not found.')
    except Exception as e:
        messages.error(request, f'Error updating approval status: {str(e)}')

    return redirect('security')


@login_required
def add_news(request):
    if request.user.position != 'landlord':
        messages.error(request, 'Only landlords can add news.')
        return redirect('news')

    if request.method == 'POST':
        try:
            # Get the landlord profile
            landlord_profile = LandLord.objects.get(user=request.user)

            # Create new news article
            news_article = News(
                author=landlord_profile,
                title=request.POST.get('title'),
                content=request.POST.get('content'),
                excerpt=request.POST.get('excerpt'),
                priority=request.POST.get('priority', 'normal'),
                category=request.POST.get('category', 'general'),
                is_published=request.POST.get('is_published') == 'on',
            )

            # Handle file upload if provided
            if request.FILES.get('featured_image'):
                news_article.featured_image = request.FILES['featured_image']

            news_article.save()
            messages.success(request, 'News article added successfully!')

        except LandLord.DoesNotExist:
            messages.error(request, 'Landlord profile not found. Please complete your profile first.')
        except Exception as e:
            messages.error(request, f'Error adding news article: {str(e)}')

    return redirect('news')


@login_required
def edit_news(request, news_id):
    if request.user.position != 'landlord':
        messages.error(request, 'Only landlords can edit news.')
        return redirect('news')

    try:
        landlord_profile = LandLord.objects.get(user=request.user)
        news_article = get_object_or_404(News, id=news_id, author=landlord_profile)

        if request.method == 'POST':
            # Update news article fields
            news_article.title = request.POST.get('title')
            news_article.content = request.POST.get('content')
            news_article.excerpt = request.POST.get('excerpt')
            news_article.priority = request.POST.get('priority', 'normal')
            news_article.category = request.POST.get('category', 'general')
            news_article.is_published = request.POST.get('is_published') == 'on'

            # Handle file upload if provided
            if request.FILES.get('featured_image'):
                news_article.featured_image = request.FILES['featured_image']

            news_article.save()
            messages.success(request, 'News article updated successfully!')
            return redirect('news')

    except LandLord.DoesNotExist:
        messages.error(request, 'Landlord profile not found.')
    except Exception as e:
        messages.error(request, f'Error updating news article: {str(e)}')

    return redirect('news')


@login_required
def delete_news(request, news_id):
    if request.user.position != 'landlord':
        messages.error(request, 'Only landlords can delete news.')
        return redirect('news')

    try:
        landlord_profile = LandLord.objects.get(user=request.user)
        news_article = get_object_or_404(News, id=news_id, author=landlord_profile)

        if request.method == 'POST':
            news_title = news_article.title
            news_article.delete()
            messages.success(request, f'News article "{news_title}" deleted successfully!')
        else:
            messages.error(request, 'Invalid request method.')

    except LandLord.DoesNotExist:
        messages.error(request, 'Landlord profile not found.')
    except Exception as e:
        messages.error(request, f'Error deleting news article: {str(e)}')

    return redirect('news')


@login_required
def view_notifications(request):
    if request.user.position != 'landlord':
        messages.error(request, 'Access denied.')
        return redirect('news')

    try:
        landlord_profile = LandLord.objects.get(user=request.user)
        notifications = BoardNotification.objects.filter(sender=landlord_profile)

        context = {
            'profile': landlord_profile,
            'notifications': notifications,
        }

        return render(request, 'dashboard/notifications.html', context)

    except LandLord.DoesNotExist:
        messages.error(request, 'Landlord profile not found.')
        return redirect('news')
