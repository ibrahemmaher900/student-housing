from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.files.storage import default_storage
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
                    if os.path.isfile(request.user.profile.profile_picture.path):
                        os.remove(request.user.profile.profile_picture.path)
                
                # حفظ الصورة الجديدة
                request.user.profile.profile_picture = profile_picture
                request.user.profile.save()
                messages.success(request, 'تم تغيير صورة البروفيل بنجاح')
            return redirect('profile')
        
        elif action == 'remove_picture':
            # حذف صورة البروفيل
            if request.user.profile.profile_picture:
                if os.path.isfile(request.user.profile.profile_picture.path):
                    os.remove(request.user.profile.profile_picture.path)
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

def view_profile(request, username):
    """عرض ملف شخصي لمستخدم آخر"""
    user = User.objects.get(username=username)
    return render(request, 'users/view_profile.html', {'user': user})
