from django.urls import path
from . import views

urlpatterns = [
    path('', views.landingpage_view, name='landingpage'),  # root URL, or change as needed
    path('aboutus/', views.aboutus_view, name='aboutus'),
    path('service/', views.service_view, name='service'),
]
