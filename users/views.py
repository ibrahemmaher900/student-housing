from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_type = form.cleaned_data.get('user_type')
            user.profile.user_type = user_type
            user.profile.save()
            
            username = form.cleaned_data.get('username')
            messages.success(request, f'تم إنشاء حساب {username} بنجاح! يمكنك الآن تسجيل الدخول.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    from apartments.models import Apartment, Booking, Wishlist, Notification
    
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            # حفظ البيانات الشخصية فقط (الاسم الأول والأخير) وليس اسم المستخدم أو البريد الإلكتروني
            user = request.user
            user.first_name = u_form.cleaned_data['first_name']
            user.last_name = u_form.cleaned_data['last_name']
            user.save(update_fields=['first_name', 'last_name'])
            
            # حفظ بيانات الملف الشخصي
            p_form.save()
            
            messages.success(request, 'تم تحديث ملفك الشخصي بنجاح!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    # جمع الإحصائيات للمستخدم
    user_stats = {}
    
    if request.user.profile.user_type == 'student':
        # إحصائيات الطالب
        user_stats['wishlist_count'] = Wishlist.objects.filter(user=request.user).count()
        user_stats['bookings_count'] = Booking.objects.filter(student=request.user).count()
        user_stats['approved_bookings'] = Booking.objects.filter(student=request.user, status='approved').count()
        user_stats['pending_bookings'] = Booking.objects.filter(student=request.user, status='pending').count()
    else:
        # إحصائيات المالك
        user_stats['apartments_count'] = Apartment.objects.filter(owner=request.user).count()
        user_stats['approved_apartments'] = Apartment.objects.filter(owner=request.user, status='approved').count()
        user_stats['pending_apartments'] = Apartment.objects.filter(owner=request.user, status='pending').count()
        user_stats['bookings_count'] = Booking.objects.filter(apartment__owner=request.user).count()
        user_stats['approved_bookings'] = Booking.objects.filter(apartment__owner=request.user, status='approved').count()
    
    # إحصائيات مشتركة
    user_stats['notifications_count'] = Notification.objects.filter(user=request.user).count()
    user_stats['unread_notifications'] = Notification.objects.filter(user=request.user, is_read=False).count()
    
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'user_stats': user_stats,
    }
    
    return render(request, 'users/profile.html', context)


def view_profile(request, user_id):
    from apartments.models import Apartment, Booking, Wishlist, Notification
    
    profile_user = get_object_or_404(User, id=user_id)
    
    # جمع الإحصائيات للمستخدم المعروض
    user_stats = {}
    
    if profile_user.profile.user_type == 'student':
        # إحصائيات الطالب
        user_stats['wishlist_count'] = Wishlist.objects.filter(user=profile_user).count()
        user_stats['bookings_count'] = Booking.objects.filter(student=profile_user).count()
    else:
        # إحصائيات المالك
        user_stats['apartments_count'] = Apartment.objects.filter(owner=profile_user).count()
        user_stats['approved_apartments'] = Apartment.objects.filter(owner=profile_user, status='approved').count()
    
    # الشقق المعروضة للمالك
    apartments = []
    if profile_user.profile.user_type == 'owner':
        apartments = Apartment.objects.filter(owner=profile_user, status='approved')[:4]
    
    context = {
        'profile_user': profile_user,
        'user_stats': user_stats,
        'apartments': apartments,
        'is_owner': profile_user.profile.user_type == 'owner',
        'is_self': request.user == profile_user
    }
    
    return render(request, 'users/view_profile.html', context)
