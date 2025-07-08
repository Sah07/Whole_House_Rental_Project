from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import PropertyForm
from .models import Property, Favorite
from booking.models import Booking 
from django.contrib.auth.decorators import login_required
from property_apps.recommender import recommend_similar_properties  # Import recommender function
from django.core.paginator import Paginator
@login_required
def add_property(request, pk=None):
    if pk:
        property_instance = get_object_or_404(Property, pk=pk, landlord=request.user)
    else:
        property_instance = None

    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=property_instance)
        if form.is_valid():
            property = form.save(commit=False)
            property.landlord = request.user
            property.save()
            if pk:
                messages.success(request, "Property updated successfully !")
            else:
                messages.success(request, "Property posted successfully !")
            return redirect('property_list')  # Or 'home' if you prefer
        else:
            messages.error(request, "Please fix the errors below and try again.")
    else:
        form = PropertyForm(instance=property_instance)

    return render(request, 'property_apps/add_property.html', {'form': form})

@login_required
def property_detail(request, pk):
    property = get_object_or_404(Property, pk=pk)

    user_favorites = []
    if request.user.is_authenticated:
        user_favorites = request.user.favorites.values_list('property_id', flat=True)

    can_book = True
    booking_status = None

    # Prevent landlord from booking own property
    if request.user == property.landlord:
        can_book = False
        booking_status = "You cannot book your own property."

    else:
    # Check if user has any active (non-rejected) booking
        active_booking = Booking.objects.filter(
            tenant=request.user,
        ).exclude(status='Rejected').first()

        if active_booking:
            if active_booking.property == property:
                booking_status = f"Your booking request for this property is {active_booking.status}."
                can_book = active_booking.status == 'Rejected'  # allow booking again only if rejected
            else:
                can_book = False
                booking_status = "You already have an active booking for another property."

    return render(request, 'property_apps/property_detail.html', {
        'property': property,
        'user_favorites': user_favorites,
        'can_book': can_book,
        'booking_status': booking_status,
    })

@login_required
def property_list_view(request):
    properties = Property.objects.filter(landlord=request.user).order_by('-available_from')

    paginator = Paginator(properties, 5)  # Show 5 properties per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'property_apps/property_list.html', {'page_obj': page_obj})

@login_required
def delete_property(request, pk):
    property_obj = get_object_or_404(Property, pk=pk, landlord=request.user)
    try:
        property_obj.delete()
        messages.success(request, "Property deleted successfully !")
    except Exception:
        messages.error(request, "Error occurred while deleting the property.")
    return redirect('property_list')

@login_required
def add_to_favorites(request, property_id):
    property_obj = get_object_or_404(Property, id=property_id)
    Favorite.objects.get_or_create(user=request.user, property=property_obj)
    messages.success(request, "Added to favorites!")
    return redirect('property_detail', pk=property_id)

@login_required
def remove_from_favorites(request, property_id):
    property_obj = get_object_or_404(Property, id=property_id)
    Favorite.objects.filter(user=request.user, property=property_obj).delete()
    messages.success(request, "Removed from favorites.")
    return redirect('property_detail', pk=property_id)

@login_required
def favorite_list(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('property')
    favorited_properties = [fav.property for fav in favorites]

    recommended_properties = recommend_similar_properties(favorites)

    return render(request, 'property_apps/favorite_list.html', {
        'favorites': favorites,
        'properties': favorited_properties,
        'recommended_properties': recommended_properties,
    })
