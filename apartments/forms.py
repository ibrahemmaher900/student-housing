from django import forms
from .models import Apartment, ApartmentImage, Booking, University, Comment

class ApartmentForm(forms.ModelForm):
    class Meta:
        model = Apartment
        exclude = ['owner', 'created_at', 'updated_at', 'status']

class ApartmentImageForm(forms.ModelForm):
    class Meta:
        model = ApartmentImage
        fields = ['image']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_date', 'end_date', 'message']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'message': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

class ApartmentSearchForm(forms.Form):
    university = forms.ModelChoiceField(queryset=University.objects.all(), required=False)
    min_price = forms.IntegerField(required=False)
    max_price = forms.IntegerField(required=False)
    apartment_type = forms.ChoiceField(choices=[('', 'جميع الأنواع'), ('studio', 'شقة'), ('room', 'غرفة'), ('bed', 'سرير')], required=False)
    bedrooms = forms.IntegerField(required=False)
    furnished = forms.BooleanField(required=False)
    has_wifi = forms.BooleanField(required=False)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

class RatingForm(forms.Form):
    rating = forms.IntegerField(min_value=1, max_value=5)
    review = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)

ReplyForm = CommentForm