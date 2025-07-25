from django import forms
from .models import Apartment, ApartmentImage, Booking, University, Comment

class ApartmentForm(forms.ModelForm):
    class Meta:
        model = Apartment
        fields = ['title', 'description', 'price', 'apartment_type', 'area', 'bedrooms', 'bathrooms', 'address', 'distance_to_university', 'university', 'furnished', 'has_wifi', 'has_ac', 'has_parking']

class ApartmentImageForm(forms.ModelForm):
    class Meta:
        model = ApartmentImage
        fields = ['image']

class ApartmentSearchForm(forms.Form):
    university = forms.ModelChoiceField(queryset=University.objects.all(), required=False, empty_label="اختر الجامعة")
    min_price = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    max_price = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    apartment_type = forms.ChoiceField(choices=[('', 'نوع السكن')] + Apartment.APARTMENT_TYPE_CHOICES, required=False)
    bedrooms = forms.IntegerField(required=False)
    furnished = forms.BooleanField(required=False)
    has_wifi = forms.BooleanField(required=False)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'اكتب تعليقك هنا...'})
        }

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_date', 'end_date', 'message']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }