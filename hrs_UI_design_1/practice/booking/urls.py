from django.urls import path
from . import views

urlpatterns = [
    path('book/<int:property_id>/', views.book_property, name='book_property'),
    path('approve/<int:booking_id>/', views.booking_approve, name='booking_approve'),
    path('reject/<int:booking_id>/', views.booking_reject, name='booking_reject'),
    path('my-rentals/', views.rentals, name='my_rentals'),
    path('cancel/<int:booking_id>/', views.booking_cancel, name='booking_cancel'),
    path('rental-requests/', views.rental_requests_view, name='rental_requests'),
    path('landlord-info/<int:landlord_id>/info/', views.view_landlord_info , name='view_landlord_info'),
]
