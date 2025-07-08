from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from property_apps.models import Property
from booking.models import Booking
import random
from django.core.mail import send_mail
from django.core.paginator import Paginator

def generate_otp():
    return str(random.randint(100000, 999999))


def homepage(request):
    properties = Property.objects.all()

    # Filtering logic
    if request.method == "GET":
        city = request.GET.get('city')
        bedrooms = request.GET.get('bedrooms')
        bathrooms = request.GET.get('bathrooms')
        furnished = request.GET.get('furnished')
        max_rent = request.GET.get('max_rent')
        address = request.GET.get('area')

        if city:
            properties = properties.filter(city__icontains=city)
        if bedrooms:
            properties = properties.filter(bedrooms=bedrooms)
        if bathrooms:
            properties = properties.filter(bathrooms=bathrooms)
        if furnished:
            if furnished.lower() == 'true':
                properties = properties.filter(furnished=True)
            elif furnished.lower() == 'false':
                properties = properties.filter(furnished=False)
        if max_rent:
            properties = properties.filter(monthly_rent__lte=max_rent)
        if address:
            properties = properties.filter(address__icontains=address)

    # Pagination: 10 properties per page
    paginator = Paginator(properties, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'Authentication/homepage.html', {'page_obj': page_obj})


def signup(request):
    if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        phone = request.POST.get('phone')
        role = request.POST.get('role')
        email = request.POST.get('email')
        password = request.POST.get('password')

        error = False
        
        # Validate unique username and email
        if User.objects.filter(username=username).exists():
            error = True
            messages.error(request, 'Username already exists')
        if User.objects.filter(email=email).exists():
            error = True
            messages.error(request, 'Email already exists')
        if len(password) < 5:
            error = True
            messages.error(request, 'Password must be at least 5 characters')

        if not error:
            new_user = User.objects.create_user(
                first_name=firstname,
                last_name=lastname,
                email=email,
                username=username,
                password=password
            )
            
            otp_code = generate_otp()
            Profile.objects.create(user=new_user, phone_num=phone, role=role, otp=otp_code)

            # Send OTP email
            send_mail(
                'Your OTP Code for Email Verification',
                f'Hello {firstname},\n\nYour OTP is: {otp_code}\n\nPlease enter this to verify your email.',
                'your_email@example.com',
                [email],
                fail_silently=False,
            )

            messages.success(request, 'OTP sent to your email. Please verify.')
            return redirect('verify-otp')
        else:
            return render(request, 'Authentication/signup.html')

    return render(request, 'Authentication/signup.html')


def verify_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        entered_otp = request.POST.get('otp')

        try:
            user = User.objects.get(email=email)
            profile = user.profile
            if profile.otp == entered_otp:
                profile.is_verified = True
                profile.otp = ''
                profile.save()
                messages.success(request, 'Email verified. You can now log in.')
                return redirect('login')
            else:
                messages.error(request, 'Invalid OTP')
        except User.DoesNotExist:
            messages.error(request, 'User not found')
    
    return render(request, 'Authentication/verify.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)

            if user is not None:
                if not user.profile.is_verified:
                    messages.error(request, 'Please verify your email before logging in.')
                    return redirect('verify-otp')

                login(request, user)
                return redirect('home')

            messages.error(request, 'Invalid email or password')
            return redirect('login')

        except User.DoesNotExist:
            messages.error(request, 'Invalid email or password')
            return redirect('login')

    return render(request, 'Authentication/login.html')


def LogoutView(request):
    logout(request)
    return redirect('login')


# @login_required
# def cancel_booking(request, property_id):
#     property_obj = get_object_or_404(Property, id=property_id)

#     # Ensure booking belongs to current user before deleting
#     Booking.objects.filter(property=property_obj, tenant=request.user).delete()

#     messages.success(request, "Your booking has been cancelled.")
#     return redirect('property_detail', pk=property_id)


# @login_required
# def rental_requests_view(request):
#     if request.user.profile.role == 'landlord':
#         landlord_properties = Property.objects.filter(landlord=request.user)
#         bookings = Booking.objects.filter(property__in=landlord_properties)
        
#         return render(request, 'booking/rental_requests.html', {'bookings': bookings})
#     else:
#         messages.error(request, "Access denied.")
#         return redirect('home')


@login_required
def search_properties_view(request):
    return render(request, 'Authentication/search_properties.html')


# @login_required
# def favorites_view(request):
#     return render(request, 'Authentication/favorites.html')


@login_required
def profile_view(request):
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    return render(request, 'Authentication/profile.html', {'user': user, 'profile': profile})


@login_required
def delete_profile(request):
    if request.method == 'POST':
        user = request.user
        try:
            profile = Profile.objects.get(user=user)
            profile.delete()
        except Profile.DoesNotExist:
            pass
        user.delete()
        logout(request)
        messages.success(request, "Your account has been deleted successfully.")
        return redirect('home')
    return redirect('profile')
