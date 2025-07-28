from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Apartment, Booking, Notification

def is_admin(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_admin)
def approve_apartment(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk)
    apartment.status = 'approved'
    apartment.save()
    
    Notification.objects.create(
        user=apartment.owner,
        notification_type='apartment_approved',
        message=f'تمت الموافقة على شقتك {apartment.title}',
        related_apartment=apartment
    )
    
    messages.success(request, 'تمت الموافقة على الشقة!')
    return redirect('admin_apartments')

@login_required
@user_passes_test(is_admin)
def reject_apartment(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk)
    apartment.status = 'rejected'
    apartment.save()
    
    Notification.objects.create(
        user=apartment.owner,
        notification_type='apartment_rejected',
        message=f'تم رفض شقتك {apartment.title}',
        related_apartment=apartment
    )
    
    messages.success(request, 'تم رفض الشقة!')
    return redirect('admin_apartments')

@login_required
def update_booking_status(request, pk, status):
    booking = get_object_or_404(Booking, pk=pk)
    
    if booking.apartment.owner != request.user:
        messages.error(request, 'ليس لديك صلاحية!')
        return redirect('owner_dashboard')
    
    if status == 'approve':
        booking.status = 'approved'
        messages.success(request, 'تمت الموافقة على الحجز!')
    elif status == 'reject':
        booking.status = 'rejected'
        messages.success(request, 'تم رفض الحجز!')
    
    booking.save()
    return redirect('owner_dashboard')

@login_required
def report_non_serious_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    
    if booking.apartment.owner != request.user:
        messages.error(request, 'ليس لديك صلاحية!')
        return redirect('owner_dashboard')
    
    booking.status = 'non_serious'
    booking.save()
    
    profile = booking.student.profile
    profile.non_serious_reports += 1
    if profile.non_serious_reports >= 3:
        profile.is_banned = True
    profile.save()
    
    messages.success(request, 'تم الإبلاغ!')
    return redirect('owner_dashboard')