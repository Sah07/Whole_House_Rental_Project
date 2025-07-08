from django.contrib import admin
from property_apps.models import Property
class PropertyAdmin(admin.ModelAdmin):
    list_display=('title','property_type','address','city','bedrooms','bathrooms','furnished','monthly_rent','available_from','image','is_available')

admin.site.register(Property,PropertyAdmin)