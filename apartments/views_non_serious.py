from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Booking

@login_required
def report_non_serious(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    
    if booking.apartment.owner == request.user:
        booking.status = 'non_serious'
        booking.save()
        
        profile = booking.student.profile
        profile.non_serious_reports += 1
        if profile.non_serious_reports >= 3:
            profile.is_banned = True
        profile.save()
        
        messages.success(request, 'تم الإبلاغ عن المستخدم')
    
    return redirect('manage_bookings')

@login_required
def unban_user(request, user_id):
    if request.user.is_staff:
        user = get_object_or_404(User, pk=user_id)
        user.profile.is_banned = False
        user.profile.non_serious_reports = 0
        user.profile.save()
        messages.success(request, 'تم إلغاء حظر المستخدم')
    
    return redirect('admin_users')