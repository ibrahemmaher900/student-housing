from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.files.storage import default_storage
from django.http import JsonResponse
from .models import Profile
from .forms import UserUpdateForm, ProfileUpdateForm
import os

@login_required
def profile(request):
    """عرض الملف الشخصي"""
    # إنشاء بروفيل إذا لم يكن موجود
    try:
        if not hasattr(request.user, 'profile'):
            Profile.objects.create(user=request.user)
    except Exception as e:
        print(f"Error creating profile: {e}")
    

    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'update_picture':
            if 'profile_picture' in request.FILES:
                try:
                    # حذف الصورة القديمة
                    if request.user.profile.profile_picture:
                        request.user.profile.profile_picture.delete(save=False)
                    
                    request.user.profile.profile_picture = request.FILES['profile_picture']
                    request.user.profile.save()
                except Exception as e:
                    messages.error(request, 'حدث خطأ في رفع الصورة')
                    print(f"Error uploading profile picture: {e}")
                    return redirect('profile')
                messages.success(request, 'تم تغيير صورة البروفيل بنجاح')
            return redirect('profile')
        
        elif action == 'remove_picture':
            try:
                if request.user.profile.profile_picture:
                    request.user.profile.profile_picture.delete(save=False)
                request.user.profile.profile_picture = None
                request.user.profile.save()
            except Exception as e:
                messages.error(request, 'حدث خطأ في حذف الصورة')
                print(f"Error removing profile picture: {e}")
                return redirect('profile')
            messages.success(request, 'تم حذف صورة البروفيل بنجاح')
            return redirect('profile')
        
        else:
            # تحديث المعلومات
            try:
                profile = request.user.profile
                profile.phone = request.POST.get('phone', '').strip() or None
                profile.city = request.POST.get('city', '').strip() or None
                profile.bio = request.POST.get('bio', '').strip() or None
                profile.save()
            except Exception as e:
                messages.error(request, 'حدث خطأ في حفظ البيانات')
                print(f"Error updating profile data: {e}")
                return redirect('profile')
            
            messages.success(request, 'تم حفظ التغييرات بنجاح')
            return redirect('profile')
    
    return render(request, 'users/profile.html')

@login_required
def profile_ajax(request):
    """معالجة طلبات AJAX للبروفيل"""
    if request.method == 'POST':
        try:
            # إنشاء بروفيل إذا لم يكن موجود
            profile, created = Profile.objects.get_or_create(user=request.user)
            
            action = request.POST.get('action')
            
            if action == 'update_picture':
                if 'profile_picture' in request.FILES:
                    profile_picture = request.FILES['profile_picture']
                    
                    # فحص حجم الملف
                    if profile_picture.size > 2 * 1024 * 1024:  # 2MB
                        return JsonResponse({'success': False, 'error': 'حجم الصورة كبير جداً'})
                    
                    profile.profile_picture = profile_picture
                    profile.save()
                    return JsonResponse({'success': True})
                return JsonResponse({'success': False, 'error': 'لم يتم رفع ملف'})
            
            elif action == 'remove_picture':
                if profile.profile_picture:
                    profile.profile_picture.delete()
                profile.profile_picture = None
                profile.save()
                return JsonResponse({'success': True})
            
            else:
                # تحديث المعلومات الإضافية
                phone = request.POST.get('phone', '').strip()
                city = request.POST.get('city', '').strip()
                bio = request.POST.get('bio', '').strip()
                
                profile.phone = phone or None
                profile.city = city or None
                profile.bio = bio or None
                profile.save()
                
                return JsonResponse({'success': True})
        
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def view_profile(request, username):
    """عرض ملف شخصي لمستخدم آخر"""
    user = User.objects.get(username=username)
    return render(request, 'users/view_profile.html', {'user': user})
