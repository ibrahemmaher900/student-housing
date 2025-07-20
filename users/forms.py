from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30, required=True, label="الاسم الأول")
    last_name = forms.CharField(max_length=30, required=True, label="الاسم الأخير")
    user_type = forms.ChoiceField(choices=Profile.USER_TYPE_CHOICES, label="نوع المستخدم")
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'user_type']
        labels = {
            'username': 'اسم المستخدم',
            'email': 'البريد الإلكتروني',
            'password1': 'كلمة المرور',
            'password2': 'تأكيد كلمة المرور',
        }

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(disabled=True, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(disabled=True, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=30, required=True, label="الاسم الأول", widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=True, label="الاسم الأخير", widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            'username': 'اسم المستخدم',
            'email': 'البريد الإلكتروني',
        }

class ProfileUpdateForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
    
    class Meta:
        model = Profile
        fields = ['phone_number', 'university', 'bio', 'profile_picture']
        labels = {
            'phone_number': 'رقم الهاتف',
            'university': 'الجامعة',
            'bio': 'نبذة شخصية',
            'profile_picture': 'الصورة الشخصية',
        }
        widgets = {
            'university': forms.Select(attrs={'class': 'form-select'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }