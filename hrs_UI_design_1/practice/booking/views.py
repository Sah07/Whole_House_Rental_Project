from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from property_apps.models import Property
from .models import Booking
from .forms import BookingForm
from django.contrib.auth.models import User
@login_required
def book_property(request, property_id):
    property_obj = get_object_or_404(Property, pk=property_id)

    if request.method == 'POST':
        # Check if property already booked (accepted)
        if Booking.objects.filter(property=property_obj, status='Accepted').exists():
            messages.error(request, "This property is already booked by another tenant.")
            return redirect('property_detail', pk=property_id)

        # Check if tenant already booked this property (pending/accepted)
        active_booking = Booking.objects.filter(
            tenant=request.user,
            property=property_obj
        ).exclude(status='Rejected').first()

        if active_booking:
            messages.error(request, "You already have an active booking for this property.")
            return redirect('property_detail', pk=property_id)

        # Process booking form
        form = BookingForm(request.POST)
        if form.is_valid():
            note = form.cleaned_data['note']
            Booking.objects.create(
                tenant=request.user,
                property=property_obj,
                status='Pending',
                note=note
            )
            messages.success(request, "Booking request sent successfully.", extra_tags='booking')
            return redirect('property_detail', pk=property_id)
        else:
            messages.error(request, "Invalid booking form.", extra_tags='booking')
            return redirect('property_detail', pk=property_id)

    return redirect('property_detail', pk=property_id)

@login_required
def booking_approve(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.user != booking.property.landlord:
        messages.error(request, " You don't have permission to approve this booking.")
        return redirect('rental_requests')

    if booking.status == 'Pending':
        booking.status = 'Accepted'
        booking.save()

        # Auto-reject all other pending bookings for this property
        Booking.objects.filter(
            property=booking.property,
            status='Pending'
        ).exclude(id=booking.id).update(status='Rejected')

        messages.success(request, "✅ Booking approved and other pending bookings rejected.")

    return redirect('rental_requests')


@login_required
def booking_reject(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.user != booking.property.landlord:
        messages.error(request, " You don't have permission to reject this booking.")
        return redirect('rental_requests')

    if booking.status == 'Pending':
        booking.status = 'Rejected'
        booking.save()
        messages.success(request, " Booking rejected.")

    return redirect('rental_requests')


@login_required
def rentals(request):
    user_role = getattr(request.user.profile, 'role', None)  # adjust this to your profile role

    if user_role == 'landlord':
        bookings = Booking.objects.filter(property__landlord=request.user)
    elif user_role == 'tenant':
        bookings = Booking.objects.filter(tenant=request.user)
    elif request.user.is_staff:
        bookings = Booking.objects.all()
    else:
        bookings = Booking.objects.none()

    return render(request, 'booking/my_rentals.html', {'bookings': bookings})


@login_required
def booking_cancel(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    # Ensure only the tenant who made the booking can cancel
    if request.user != booking.tenant:
        messages.error(request, "You don't have permission to cancel this booking.")
        return redirect('property_detail', pk=booking.property.id)

    if request.method == 'POST':
        if booking.status == 'Pending':
            booking.delete()  #  DELETE instead of setting 'Rejected'
            messages.success(request, "Your booking has been cancelled.")
        elif booking.status == 'Accepted':
            messages.warning(request, "You cannot cancel an approved booking.")  # Optional rule
        else:
            messages.warning(request, "This booking cannot be cancelled.")

    return redirect('property_detail', pk=booking.property.id)

@login_required
def rental_requests_view(request):
    if hasattr(request.user, 'profile') and request.user.profile.role == 'landlord':
        landlord_properties = Property.objects.filter(landlord=request.user)
        bookings = Booking.objects.filter(property__in=landlord_properties)
        return render(request, 'booking/rental_requests.html', {'bookings': bookings})
    else:
        messages.error(request, "Access denied.")
        return redirect('home')
@login_required
def view_landlord_info(request, landlord_id):
    landlord = get_object_or_404(User, id=landlord_id)
    
    # Optional: Add a check to ensure the user has an accepted booking with this landlord
    from booking.models import Booking
    has_access = Booking.objects.filter(tenant=request.user, property__landlord=landlord, status='Accepted').exists()
    
    if not has_access:
        messages.error(request, "You don't have access to this landlord's info.")
        return redirect('my_rentals')  # or 'home'

    return render(request, 'booking/landlord_info.html', {'landlord': landlord})