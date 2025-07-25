from django import forms
from .models import Apartment, ApartmentImage, Booking, University

class SimpleApartmentForm(forms.Form):
    title = forms.CharField(max_length=100, required=True)
    description = forms.CharField(widget=forms.Textarea, required=False)
    price = forms.DecimalField(max_digits=10, decimal_places=2, required=True)
    apartment_type = forms.CharField(max_length=10, initial='studio')
    area = forms.IntegerField(required=True)
    bedrooms = forms.IntegerField(initial=1)
    bathrooms = forms.IntegerField(initial=1)
    address = forms.CharField(max_length=200, required=True)
    distance_to_university = forms.DecimalField(max_digits=5, decimal_places=2, required=True)
    university = forms.ModelChoiceField(queryset=University.objects.all(), required=True)
    furnished = forms.BooleanField(required=False)
    has_wifi = forms.BooleanField(required=False)
    has_ac = forms.BooleanField(required=False)
    has_parking = forms.BooleanField(required=False)
    images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=True)

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_date', 'end_date', 'message']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }