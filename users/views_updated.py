from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from django.http import JsonResponse
from .models import Profile
from .forms_updated import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            user_type = form.cleaned_data.get('user_type')
            
            # تسجيل دخول المستخدم تلقائياً
            login(request, user)
            
            user_type_display = 'طالب' if user_type == 'student' else 'مالك عقار'
            messages.success(request, f'تم إنشاء حسابك بنجاح كـ {user_type_display}!')
            
            # توجيه المستخدم حسب نوع الحساب
            if user_type == 'owner':
                return redirect('owner_dashboard')
            else:
                return redirect('apartment_list')
    else:
        form = UserRegisterForm()
    
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    try:
        # إنشاء بروفيل إذا لم يكن موجود
        profile, created = Profile.objects.get_or_create(user=request.user)
        
        if request.method == 'POST':
            user_form = UserUpdateForm(request.POST, instance=request.user)
            profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
            
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, 'تم تحديث الملف الشخصي بنجاح!')
                return redirect('profile')
        else:
            user_form = UserUpdateForm(instance=request.user)
            profile_form = ProfileUpdateForm(instance=profile)
        
        context = {
            'user_form': user_form,
            'profile_form': profile_form,
            'profile': profile
        }
        return render(request, 'users/profile.html', context)
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
                    profile.save(update_fields=['profile_picture'])
                    return JsonResponse({
                        'success': True, 
                        'new_url': profile.get_profile_picture_url()
                    })
                return JsonResponse({'success': False, 'error': 'لم يتم رفع ملف'})
            
            elif action == 'remove_picture':
                profile.profile_picture = None
                profile.save(update_fields=['profile_picture'])
                return JsonResponse({
                    'success': True,
                    'new_url': profile.get_profile_picture_url()
                })
            
            elif action == 'update_info':
                profile.phone = request.POST.get('phone', '')
                profile.city = request.POST.get('city', '')
                profile.bio = request.POST.get('bio', '')
                profile.save(update_fields=['phone', 'city', 'bio'])
                return JsonResponse({'success': True})
        
        return JsonResponse({'success': False, 'error': 'طلب غير صحيح'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def view_profile(request, username):
    try:
        user = get_object_or_404(User, username=username)
        profile, created = Profile.objects.get_or_create(user=user)
        
        # إحصائيات المستخدم
        stats = {}
        if profile.user_type == 'owner':
            stats = {
                'total_apartments': user.apartments.count(),
                'approved_apartments': user.apartments.filter(status='approved').count(),
                'total_bookings': user.apartments.aggregate(
                    total=models.Count('bookings')
                )['total'] or 0
            }
        else:  # student
            stats = {
                'total_bookings': user.bookings.count(),
                'approved_bookings': user.bookings.filter(status='approved').count(),
                'wishlist_count': user.wishlists.count()
            }
        
        context = {
            'profile_user': user,
            'profile': profile,
            'stats': stats
        }
        return render(request, 'users/view_profile.html', context)
    except Exception as e:
        messages.error(request, 'المستخدم غير موجود')
        return redirect('home')

@login_required
def change_password(request):
    """تغيير كلمة المرور"""
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')
        
        if not request.user.check_password(old_password):
            messages.error(request, 'كلمة المرور الحالية غير صحيحة')
        elif new_password1 != new_password2:
            messages.error(request, 'كلمات المرور الجديدة غير متطابقة')
        elif len(new_password1) < 8:
            messages.error(request, 'كلمة المرور يجب أن تكون 8 أحرف على الأقل')
        else:
            request.user.set_password(new_password1)
            request.user.save()
            messages.success(request, 'تم تغيير كلمة المرور بنجاح')
            return redirect('login')
    
    return render(request, 'users/change_password.html')