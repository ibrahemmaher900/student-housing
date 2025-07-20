from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Booking, Notification, Apartment

@login_required
def report_non_serious(request, booking_id):
    """وظيفة للإبلاغ عن مستخدم غير جاد في الحجز"""
    booking = get_object_or_404(Booking, pk=booking_id)
    
    # التحقق من أن المستخدم هو مالك الشقة
    if booking.apartment.owner != request.user:
        messages.error(request, 'ليس لديك صلاحية الإبلاغ عن هذا الحجز.')
        return redirect('manage_bookings')
    
    # تغيير حالة الحجز إلى غير جاد
    booking.status = 'non_serious'
    booking.save()
    
    # إنشاء تنبيه للطالب
    Notification.objects.create(
        user=booking.student,
        notification_type='non_serious_booking',
        message=f'تم الإبلاغ عنك كمستخدم غير جاد في حجز {booking.apartment.title}.',
        related_booking=booking,
        related_apartment=booking.apartment
    )
    
    # إعادة الشقة للحالة المتاحة
    apartment = booking.apartment
    apartment.available = True
    apartment.save()
    
    messages.success(request, 'تم الإبلاغ عن المستخدم كغير جاد في الحجز وتمت إعادة الشقة للحالة المتاحة.')
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'message': 'تم الإبلاغ عن المستخدم كغير جاد في الحجز وتمت إعادة الشقة للحالة المتاحة.'
        })
    
    return redirect('manage_bookings')

@login_required
def unban_user(request, user_id):
    """وظيفة لإلغاء حظر مستخدم (للمسؤولين فقط)"""
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, 'ليس لديك صلاحية إلغاء حظر المستخدمين.')
        return redirect('home')
    
    user = get_object_or_404(User, pk=user_id)
    
    # إلغاء الحظر وإعادة ضبط عداد عدم الجدية
    user.profile.is_banned = False
    user.profile.non_serious_reports = 0
    user.profile.save()
    
    # إنشاء تنبيه للمستخدم
    Notification.objects.create(
        user=user,
        notification_type='user_banned',
        message='تم إلغاء الحظر عنك. يمكنك الآن استخدام نظام الحجز مرة أخرى.',
    )
    
    messages.success(request, f'تم إلغاء الحظر عن المستخدم {user.username} بنجاح.')
    return redirect('admin_users')  # يجب إنشاء هذه الصفحة لإدارة المستخدمين