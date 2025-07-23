from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

def login_pro(request):
    """وظيفة تسجيل الدخول المحسنة"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # إذا لم يتم تحديد "تذكرني"، اجعل الجلسة تنتهي عند إغلاق المتصفح
            if not remember:
                request.session.set_expiry(0)
            
            # التحقق من نوع المستخدم
            try:
                profile = user.profile
                user_type = profile.user_type
                
                # توجيه المستخدم بناءً على نوعه
                if user_type == 'owner':
                    return redirect('my_apartments')  # صفحة شققي
                else:
                    return redirect('home')  # الصفحة الرئيسية
            except Exception as e:
                # في حالة حدوث خطأ، توجيه إلى الصفحة الرئيسية
                return redirect('home')
        else:
            messages.error(request, 'اسم المستخدم أو كلمة المرور غير صحيحة')
    
    return render(request, 'users/login_pro.html')

def register_pro(request):
    """وظيفة التسجيل المحسنة"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        user_type = request.POST.get('user_type', 'student')
        
        # التحقق من البيانات
        errors = []
        
        if User.objects.filter(username=username).exists():
            errors.append('اسم المستخدم موجود بالفعل')
        
        if User.objects.filter(email=email).exists():
            errors.append('البريد الإلكتروني مستخدم بالفعل')
        
        if password1 != password2:
            errors.append('كلمات المرور غير متطابقة')
        
        if len(password1) < 8:
            errors.append('كلمة المرور يجب أن تكون على الأقل 8 أحرف')
        
        # إذا كانت هناك أخطاء، عرضها
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'users/register_pro.html')
        
        # إنشاء المستخدم
        user = User.objects.create_user(username=username, email=email, password=password1)
        
        # تحديث نوع المستخدم
        profile = user.profile
        profile.user_type = user_type
        profile.save()
        
        messages.success(request, f'تم إنشاء حساب لـ {username}! يمكنك الآن تسجيل الدخول.')
        return redirect('login')
    
    return render(request, 'users/register_pro.html')

def logout_pro(request):
    """وظيفة تسجيل الخروج المحسنة"""
    logout(request)
    messages.success(request, 'تم تسجيل الخروج بنجاح')
    return redirect('home')
