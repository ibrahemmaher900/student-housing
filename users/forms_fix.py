from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterFormFixed(UserCreationForm):
    """نموذج تسجيل المستخدم المحسن"""
    email = forms.EmailField()
    user_type = forms.ChoiceField(
        choices=[('student', 'طالب'), ('owner', 'مالك عقار')],
        widget=forms.RadioSelect,
        initial='student',
        label='نوع المستخدم'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'user_type']
