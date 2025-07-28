from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from .models import Profile

@login_required
def profile(request):
    try:
        # إنشاء بروفيل إذا لم يكن موجود
        profile, created = Profile.objects.get_or_create(user=request.user)
        
        if request.method == 'POST':
            action = request.POST.get('action')
            
            if action == 'update_picture':
                if 'profile_picture' in request.FILES:
                    profile.profile_picture = request.FILES['profile_picture']
                    profile.save()
                    messages.success(request, 'تم تغيير صورة البروفيل')
                return redirect('profile')
            
            elif action == 'remove_picture':
                profile.profile_picture = None
                profile.save()
                messages.success(request, 'تم حذف صورة البروفيل')
                return redirect('profile')
            
            else:
                profile.phone = request.POST.get('phone', '')
                profile.city = request.POST.get('city', '')
                profile.bio = request.POST.get('bio', '')
                profile.save()
                messages.success(request, 'تم حفظ التغييرات')
                return redirect('profile')
        
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