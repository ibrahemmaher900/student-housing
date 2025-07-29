from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from .models import Apartment, Booking, Notification
from .views_notifications import create_notification

def is_admin(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    context = {
        'total_users': User.objects.count(),
        'total_apartments': Apartment.objects.count(),
        'pending_apartments': Apartment.objects.filter(status='pending').count(),
        'approved_apartments': Apartment.objects.filter(status='approved').count(),
        'rejected_apartments': Apartment.objects.filter(status='rejected').count(),
        'total_bookings': Booking.objects.count(),
        'pending_bookings': Booking.objects.filter(status='pending').count(),
        'approved_bookings': Booking.objects.filter(status='approved').count(),
        'rejected_bookings': Booking.objects.filter(status='rejected').count(),
        'students_count': User.objects.filter(profile__user_type='student').count(),
        'owners_count': User.objects.filter(profile__user_type='owner').count(),
        'recent_apartments': Apartment.objects.filter(status='pending').order_by('-created_at')[:5],
        'recent_bookings': Booking.objects.filter(status='pending').order_by('-created_at')[:5],
    }
    return render(request, 'apartments/admin_dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def admin_apartments(request):
    pending_apartments = Apartment.objects.filter(status='pending').select_related('owner', 'university').order_by('-created_at')
    approved_apartments = Apartment.objects.filter(status='approved').select_related('owner', 'university').order_by('-created_at')
    rejected_apartments = Apartment.objects.filter(status='rejected').select_related('owner', 'university').order_by('-created_at')
    
    # إحصائيات سريعة
    stats = {
        'pending_count': pending_apartments.count(),
        'approved_count': approved_apartments.count(),
        'rejected_count': rejected_apartments.count(),
        'total_count': Apartment.objects.count()
    }
    
    context = {
        'pending_apartments': pending_apartments,
        'approved_apartments': approved_apartments,
        'rejected_apartments': rejected_apartments,
        'stats': stats,
    }
    return render(request, 'apartments/admin_apartments.html', context)

@login_required
@user_passes_test(is_admin)
def approve_apartment(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk)
    
    if apartment.status == 'approved':
        messages.info(request, 'الشقة معتمدة مسبقاً')
        return redirect('admin_apartments')
    
    apartment.status = 'approved'
    apartment.save(update_fields=['status'])
    
    # إنشاء تنبيه للمالك
    create_notification(
        user=apartment.owner,
        notification_type='apartment_approved',
        message=f'تمت الموافقة على إعلانك: {apartment.title}',
        related_apartment=apartment
    )
    
    messages.success(request, f'تمت الموافقة على شقة "{apartment.title}" بنجاح!')
    return redirect('admin_apartments')

@login_required
@user_passes_test(is_admin)
def reject_apartment(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk)
    
    if apartment.status == 'rejected':
        messages.info(request, 'الشقة مرفوضة مسبقاً')
        return redirect('admin_apartments')
    
    apartment.status = 'rejected'
    apartment.save(update_fields=['status'])
    
    # إنشاء تنبيه للمالك
    create_notification(
        user=apartment.owner,
        notification_type='apartment_rejected',
        message=f'تم رفض إعلانك: {apartment.title}',
        related_apartment=apartment
    )
    
    messages.success(request, f'تم رفض شقة "{apartment.title}" بنجاح!')
    return redirect('admin_apartments')

@login_required
@user_passes_test(is_admin)
@require_POST
def bulk_approve_apartments(request):
    """الموافقة على عدة شقق دفعة واحدة"""
    apartment_ids = request.POST.getlist('apartment_ids')
    apartments = Apartment.objects.filter(id__in=apartment_ids, status='pending')
    
    approved_count = 0
    for apartment in apartments:
        apartment.status = 'approved'
        apartment.save(update_fields=['status'])
        
        # إنشاء تنبيه للمالك
        create_notification(
            user=apartment.owner,
            notification_type='apartment_approved',
            message=f'تمت الموافقة على إعلانك: {apartment.title}',
            related_apartment=apartment
        )
        approved_count += 1
    
    return JsonResponse({'success': True, 'approved_count': approved_count})

@login_required
@user_passes_test(is_admin)
@require_POST
def bulk_reject_apartments(request):
    """رفض عدة شقق دفعة واحدة"""
    apartment_ids = request.POST.getlist('apartment_ids')
    apartments = Apartment.objects.filter(id__in=apartment_ids, status='pending')
    
    rejected_count = 0
    for apartment in apartments:
        apartment.status = 'rejected'
        apartment.save(update_fields=['status'])
        
        # إنشاء تنبيه للمالك
        create_notification(
            user=apartment.owner,
            notification_type='apartment_rejected',
            message=f'تم رفض إعلانك: {apartment.title}',
            related_apartment=apartment
        )
        rejected_count += 1
    
    return JsonResponse({'success': True, 'rejected_count': rejected_count})

@login_required
@user_passes_test(is_admin)
def admin_users(request):
    """إدارة المستخدمين"""
    students = User.objects.filter(profile__user_type='student').select_related('profile').order_by('-date_joined')
    owners = User.objects.filter(profile__user_type='owner').select_related('profile').order_by('-date_joined')
    
    context = {
        'students': students,
        'owners': owners,
        'students_count': students.count(),
        'owners_count': owners.count(),
    }
    return render(request, 'apartments/admin_users.html', context)

@login_required
@user_passes_test(is_admin)
@require_POST
def toggle_user_ban(request, user_id):
    """حظر/إلغاء حظر مستخدم"""
    user = get_object_or_404(User, id=user_id)
    profile = user.profile
    
    profile.is_banned = not profile.is_banned
    profile.save(update_fields=['is_banned'])
    
    status = 'محظور' if profile.is_banned else 'غير محظور'
    
    # إنشاء تنبيه للمستخدم
    if profile.is_banned:
        create_notification(
            user=user,
            notification_type='user_banned',
            message='تم حظر حسابك من النظام',
        )
    
    return JsonResponse({
        'success': True, 
        'status': status,
        'is_banned': profile.is_banned
    })