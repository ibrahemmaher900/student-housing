from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.files.storage import default_storage
from django.http import JsonResponse
from .forms import UserUpdateForm, ProfileUpdateForm
import os

@login_required
def profile(request):
    """عرض الملف الشخصي"""
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'update_picture':
            # تغيير صورة البروفيل
            if 'profile_picture' in request.FILES:
                profile_picture = request.FILES['profile_picture']
                
                # حذف الصورة القديمة
                if request.user.profile.profile_picture:
                    try:
                        if os.path.isfile(request.user.profile.profile_picture.path):
                            os.remove(request.user.profile.profile_picture.path)
                    except:
                        pass
                
                # حفظ الصورة الجديدة
                request.user.profile.profile_picture = profile_picture
                request.user.profile.save()
                messages.success(request, 'تم تغيير صورة البروفيل بنجاح')
            return redirect('profile')
        
        elif action == 'remove_picture':
            # حذف صورة البروفيل
            if request.user.profile.profile_picture:
                try:
                    if os.path.isfile(request.user.profile.profile_picture.path):
                        os.remove(request.user.profile.profile_picture.path)
                except:
                    pass
                request.user.profile.profile_picture = None
                request.user.profile.save()
                messages.success(request, 'تم حذف صورة البروفيل بنجاح')
            return redirect('profile')
        
        else:
            # تحديث المعلومات الإضافية
            phone = request.POST.get('phone', '')
            city = request.POST.get('city', '')
            bio = request.POST.get('bio', '')
            
            profile = request.user.profile
            profile.phone = phone
            profile.city = city
            profile.bio = bio
            profile.save()
            
            messages.success(request, 'تم حفظ التغييرات بنجاح')
            return redirect('profile')
    
    return render(request, 'users/profile.html')

@login_required
def profile_ajax(request):
    """معالجة طلبات AJAX للبروفيل"""
    if request.method == 'POST':
        try:
            action = request.POST.get('action')
            
            if action == 'update_picture':
                if 'profile_picture' in request.FILES:
                    profile_picture = request.FILES['profile_picture']
                    request.user.profile.profile_picture = profile_picture
                    request.user.profile.save(update_fields=['profile_picture'])
                    return JsonResponse({'success': True})
                return JsonResponse({'success': False, 'error': 'No file uploaded'})
            
            elif action == 'remove_picture':
                request.user.profile.profile_picture = None
                request.user.profile.save(update_fields=['profile_picture'])
                return JsonResponse({'success': True})
            
            else:
                # تحديث المعلومات الإضافية
                phone = request.POST.get('phone', '').strip()
                city = request.POST.get('city', '').strip()
                bio = request.POST.get('bio', '').strip()
                
                request.user.profile.phone = phone
                request.user.profile.city = city
                request.user.profile.bio = bio
                request.user.profile.save(update_fields=['phone', 'city', 'bio'])
                
                return JsonResponse({'success': True})
        
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})

def view_profile(request, username):
    """عرض ملف شخصي لمستخدم آخر"""
    user = User.objects.get(username=username)
    return render(request, 'users/view_profile.html', {'user': user})
