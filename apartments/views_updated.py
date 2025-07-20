@login_required
def update_booking_status(request, pk, status):
    booking = get_object_or_404(Booking, pk=pk)
    
    # التحقق من أن المستخدم هو مالك الشقة
    if booking.apartment.owner != request.user:
        messages.error(request, 'ليس لديك صلاحية تحديث حالة هذا الحجز.')
        return redirect('manage_bookings')
    
    notification_type = ''
    notification_message = ''
    
    if status == 'approve':
        booking.status = 'approved'
        notification_type = 'booking_approved'
        notification_message = f'تمت الموافقة على طلب حجزك لشقة {booking.apartment.title}'
        messages.success(request, 'تمت الموافقة على الحجز بنجاح!')
    elif status == 'reject':
        booking.status = 'rejected'
        notification_type = 'booking_rejected'
        notification_message = f'تم رفض طلب حجزك لشقة {booking.apartment.title}'
        messages.success(request, 'تم رفض الحجز بنجاح!')
    elif status == 'non_serious':
        booking.status = 'non_serious'
        notification_type = 'non_serious_booking'
        
        # زيادة عداد عدم الجدية وتجميد الحساب عند تجاوز 3 مرات
        student_profile = booking.student.profile
        student_profile.non_serious_reports += 1
        
        if student_profile.non_serious_reports >= 3:
            student_profile.is_banned = True
            notification_message = f'تم الإبلاغ عنك كمستخدم غير جاد في حجز {booking.apartment.title}. تم تجميد حسابك بسبب تكرار عدم الجدية في الحجز. يرجى التواصل مع إدارة الموقع.'
            messages.success(request, 'تم الإبلاغ عن المستخدم كغير جاد في الحجز وتم تجميد حسابه بسبب تكرار عدم الجدية.')
            
            # إرسال إشعار للمسؤولين
            from django.contrib.auth.models import User
            admins = User.objects.filter(is_staff=True) | User.objects.filter(is_superuser=True)
            for admin in admins:
                Notification.objects.create(
                    user=admin,
                    notification_type='user_banned',
                    message=f'تم تجميد حساب {booking.student.username} بسبب تكرار عدم الجدية في الحجز.',
                )
        else:
            notification_message = f'تم الإبلاغ عنك كمستخدم غير جاد في حجز {booking.apartment.title}'
            messages.success(request, 'تم الإبلاغ عن المستخدم كغير جاد في الحجز.')
        
        student_profile.save()
        
        # إعادة الشقة للحالة المتاحة
        apartment = booking.apartment
        apartment.available = True
        apartment.save()
    
    booking.save()
    
    # إنشاء تنبيه للطالب فقط إذا تم تعيين نوع الإشعار
    if notification_type and notification_message:
        student_notification = Notification(
            user=booking.student,
            notification_type=notification_type,
            message=notification_message,
            related_booking=booking,
            related_apartment=booking.apartment
        )
        student_notification.save()
    
    return redirect('manage_bookings')