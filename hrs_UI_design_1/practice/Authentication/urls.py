from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path("home/", views.homepage, name='home'),

    # Auth views
    path("login/", views.login_view, name='login'),
    path("signup/", views.signup, name='signup'),
    path("logout/", views.LogoutView, name='logout'),
    path("verify/", views.verify_otp, name='verify-otp'),

    # User profile & account management
    path("profile/", views.profile_view, name="profile"),
    path("delete-account/", views.delete_profile, name='delete_profile'),

    # Property search (if really auth-only)
    path("search-properties/", views.search_properties_view, name='search_properties'),

    # Other non-booking, non-property views (remove those related to booking)
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
