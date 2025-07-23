from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view_fixed(request):
    """عرض تسجيل الدخول المحسن"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # طباعة معلومات تصحيح الأخطاء
            print(f"User logged in: {username}")
            
            # التحقق من نوع المستخدم
            try:
                profile = user.profile
                user_type = profile.user_type
                print(f"User type: {user_type}")
                
                # توجيه المستخدم بناءً على نوعه
                if user_type == 'owner':
                    return redirect('my_apartments')  # صفحة شققي
                else:
                    return redirect('home')  # الصفحة الرئيسية
            except Exception as e:
                print(f"Error checking user type: {e}")
                # في حالة حدوث خطأ، توجيه إلى الصفحة الرئيسية
                return redirect('home')
        else:
            messages.error(request, 'اسم المستخدم أو كلمة المرور غير صحيحة')
    
    return render(request, 'users/login.html')
