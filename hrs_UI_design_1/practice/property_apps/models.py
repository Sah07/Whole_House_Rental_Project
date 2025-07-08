from django.db import models
from django.contrib.auth.models import User

class Property(models.Model):
    PROPERTY_TYPES = [
        ('Apartment', 'Apartment'),
        ('Room', 'Room')
    ]
    landlord = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    title = models.CharField(max_length=100)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100, blank=True, null=True)  # City is optional
    bedrooms = models.IntegerField()  # Added the 'bedrooms' field
    bathrooms = models.IntegerField()  # Added the 'bathrooms' field
    furnished = models.BooleanField(default=False)
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2)  # Added the 'monthly_rent' field
    available_from = models.DateField()  # Added the 'available_from' field
    
    image = models.ImageField(upload_to='property_images/', blank=True, null=True)
    is_available = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        """Override the save method to extract city from the address before saving"""
        if ',' in self.address:
            self.city = self.address.split(',')[0].strip()  # Extract city from the address
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.available_from})"

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    property = models.ForeignKey("property_apps.Property", on_delete=models.CASCADE, related_name='favorited_by')
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'property')

    def __str__(self):
        return f"{self.user.username} - {self.property}"
