from django import forms
from .models import Apartment, ApartmentImage, Booking, University, Comment, Rating

class ApartmentForm(forms.ModelForm):
    class Meta:
        model = Apartment
        exclude = ['owner', 'created_at', 'updated_at', 'status']
        labels = {
            'title': 'عنوان الإعلان',
            'description': 'وصف الشقة',
            'price': 'السعر الشهري (جنيه مصري)',
            'apartment_type': 'نوع السكن',
            'area': 'المساحة بالمتر المربع',
            'bedrooms': 'عدد غرف النوم',
            'bathrooms': 'عدد الحمامات',
            'address': 'العنوان',
            'latitude': 'خط العرض',
            'longitude': 'خط الطول',
            'distance_to_university': 'المسافة للجامعة (كم)',
            'university': 'الجامعة القريبة',
            'available': 'متاح',
            'furnished': 'مفروش',
            'has_wifi': 'يوجد واي فاي',
            'has_ac': 'يوجد تكييف',
            'has_parking': 'يوجد موقف سيارات',
            'gender': 'مخصص لـ',
            'payment_method': 'طريقة الدفع',
            'deposit': 'مبلغ التأمين (جنيه مصري)',
            'bills_included': 'تشمل الفواتير',
            'max_people': 'الحد الأقصى للأشخاص',
            'floor': 'الطابق',
            'conditions': 'شروط السكن',
            'additional_description': 'وصف إضافي',
            'contact_name': 'اسم المعلن',
            'phone': 'رقم الهاتف',
            'whatsapp_available': 'متاح على واتساب',
            'advertiser_type': 'نوع المعلن',
            'additional_contact': 'طرق تواصل إضافية',
            'google_maps_link': 'رابط خرائط جوجل',
            'has_fridge': 'يوجد ثلاجة',
            'has_washer': 'يوجد غسالة',
            'has_kitchen': 'يوجد مطبخ',
            'has_private_bathroom': 'يوجد حمام خاص',
            'has_balcony': 'يوجد بلكونة',
        }
        widgets = {
            'latitude': forms.NumberInput(attrs={'step': '0.000001'}),
            'longitude': forms.NumberInput(attrs={'step': '0.000001'}),
            'walking_time': forms.NumberInput(attrs={'min': '1', 'placeholder': 'الوقت بالدقائق'}),
            'driving_time': forms.NumberInput(attrs={'min': '1', 'placeholder': 'الوقت بالدقائق'}),
            'conditions': forms.Textarea(attrs={'rows': 3}),
            'additional_description': forms.Textarea(attrs={'rows': 3}),
            'additional_contact': forms.Textarea(attrs={'rows': 2}),
        }

class ApartmentImageForm(forms.ModelForm):
    image = forms.ImageField(label='صورة الشقة')
    
    class Meta:
        model = ApartmentImage
        fields = ['image']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_date', 'end_date', 'message']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'start_date': 'تاريخ البداية',
            'end_date': 'تاريخ النهاية',
            'message': 'رسالة للمالك',
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': 'التعليق',
        }
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'اكتب تعليقك هنا...'}),
        }

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': 'الرد',
        }
        widgets = {
            'content': forms.Textarea(attrs={'rows': 2, 'class': 'form-control', 'placeholder': 'اكتب ردك هنا...'}),
        }

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['stars', 'review']
        labels = {
            'stars': 'التقييم',
            'review': 'المراجعة',
        }
        widgets = {
            'stars': forms.RadioSelect(attrs={'class': 'rating-input'}),
            'review': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'اكتب مراجعتك هنا...'}),
        }

class ApartmentSearchForm(forms.Form):
    university = forms.ModelChoiceField(
        queryset=University.objects.all(),
        required=False,
        label='الجامعة',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    min_price = forms.DecimalField(
        required=False,
        label='الحد الأدنى للسعر',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    max_price = forms.DecimalField(
        required=False,
        label='الحد الأقصى للسعر',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    apartment_type = forms.ChoiceField(
        choices=[('', 'الكل')] + list(Apartment.APARTMENT_TYPE_CHOICES),
        required=False,
        label='نوع السكن',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    bedrooms = forms.IntegerField(
        required=False,
        label='عدد غرف النوم',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '0'})
    )
    furnished = forms.BooleanField(
        required=False,
        label='مفروش',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    has_wifi = forms.BooleanField(
        required=False,
        label='يوجد واي فاي',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )