from django.shortcuts import render, redirect
from django.contrib import messages
from .forms_fix import UserRegisterFormFixed

def register_fixed(request):
    """عرض التسجيل المحسن"""
    if request.method == 'POST':
        form = UserRegisterFormFixed(request.POST)
        if form.is_valid():
            user = form.save()
            
            # استخراج نوع المستخدم من النموذج
            user_type = form.cleaned_data.get('user_type')
            
            # تحديث ملف المستخدم الشخصي
            profile = user.profile
            profile.user_type = user_type
            profile.save()
            
            username = form.cleaned_data.get('username')
            messages.success(request, f'تم إنشاء حساب لـ {username}! يمكنك الآن تسجيل الدخول.')
            return redirect('login')
    else:
        form = UserRegisterFormFixed()
    return render(request, 'users/register.html', {'form': form})
