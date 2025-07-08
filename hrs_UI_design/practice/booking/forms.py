from django import forms

class BookingForm(forms.Form):
    note = forms.CharField(
        required=True,  #  now it's mandatory!
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Write a message for the landlord...'
        })
    )
