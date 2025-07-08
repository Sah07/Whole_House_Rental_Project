from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Route to add a new property (only for logged-in users, view handles that)
    path('add-property/', views.add_property, name='add_property'),
    path('my-properties/', views.property_list_view, name='property_list'),
    path('delete-property/<int:pk>/', views.delete_property, name='delete_property'),
    path('edit-property/<int:pk>/', views.add_property, name='edit_property'),
    # View details of a specific property
    path('property/<int:pk>/', views.property_detail, name='property_detail'),
    path('favorites/add/<int:property_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('favorites/remove/<int:property_id>/', views.remove_from_favorites, name='remove_from_favorites'),
    path('favorites/', views.favorite_list, name='favorite_list'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
