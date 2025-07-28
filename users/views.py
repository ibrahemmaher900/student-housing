from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from .models import Profile

@login_required
def profile(request):
    try:
        profile, created = Profile.objects.get_or_create(user=request.user)
        if request.method == 'POST':
            action = request.POST.get('action')
            if action == 'update_picture':
                if 'profile_picture' in request.FILES:
                    profile.profile_picture = request.FILES['profile_picture']
                    profile.save()
                    messages.success(request, 'تم تغيير صورة البروفايل')
                return redirect('profile')
            elif action == 'remove_picture':
                profile.profile_picture = None
                profile.save()
                messages.success(request, 'تم حذف صورة البروفايل')
                return redirect('profile')
            elif action == 'change_password':
                old_password = request.POST.get('old_password')
                new_password1 = request.POST.get('new_password1')
                new_password2 = request.POST.get('new_password2')
                if not request.user.check_password(old_password):
                    messages.error(request, 'كلمة المرور الحالية غير صحيحة')
                    return redirect('profile')
                if new_password1 != new_password2:
                    messages.error(request, 'كلمتا المرور الجديدتان غير متطابقتين')
                    return redirect('profile')
                if len(new_password1) < 8:
                    messages.error(request, 'كلمة المرور الجديدة يجب أن تكون 8 أحرف على الأقل')
                    return redirect('profile')
                request.user.set_password(new_password1)
                request.user.save()
                messages.success(request, 'تم تغيير كلمة المرور بنجاح. يرجى تسجيل الدخول مجددًا.')
                from django.contrib.auth import logout
                logout(request)
                return redirect('login')
        return render(request, 'users/profile.html')
    except Exception as e:
        messages.error(request, 'حدث خطأ في تحميل الملف الشخصي')
        return redirect('home')

@login_required
def profile_ajax(request):
    try:
        profile, created = Profile.objects.get_or_create(user=request.user)
        
        if request.method == 'POST':
            action = request.POST.get('action')
            
            if action == 'update_picture':
                if 'profile_picture' in request.FILES:
                    profile.profile_picture = request.FILES['profile_picture']
                    profile.save()
                    return JsonResponse({'success': True})
                return JsonResponse({'success': False, 'error': 'لم يتم رفع ملف'})
            
            elif action == 'remove_picture':
                profile.profile_picture = None
                profile.save()
                return JsonResponse({'success': True})
            
            else:
                profile.phone = request.POST.get('phone', '')
                profile.city = request.POST.get('city', '')
                profile.bio = request.POST.get('bio', '')
                profile.save()
                return JsonResponse({'success': True})
        
        return JsonResponse({'success': False, 'error': 'Invalid request'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def view_profile(request, username):
    try:
        user = get_object_or_404(User, username=username)
        profile, created = Profile.objects.get_or_create(user=user)
        return render(request, 'users/view_profile.html', {'user': user, 'profile': profile})
    except Exception as e:
        messages.error(request, 'المستخدم غير موجود')
        return redirect('home')