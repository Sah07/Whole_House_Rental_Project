from django import forms
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile
from .models import Property

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'title', 'property_type', 'address', 'city', 'bedrooms',
            'bathrooms', 'furnished', 'monthly_rent', 'available_from','image', 'is_available'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 2BHK Apartment in Baneshwor'}),
            'property_type': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full address'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City name'}),
            'bedrooms': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Number of bedrooms'}),
            'bathrooms': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Number of bathrooms'}),
            
            'monthly_rent': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Rent amount'}),
            'available_from': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            # 'owner_contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact number'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            
        }
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Only check content type if it's a new uploaded file
            if isinstance(image, UploadedFile):
                if not image.content_type.startswith('image'):
                    raise ValidationError('Only image files are allowed.')
                if image.size > 5 * 1024 * 1024:  # 5MB
                    raise ValidationError('Image file too large (max 5MB).')
        return image

