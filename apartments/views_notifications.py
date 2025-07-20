from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.http import require_POST
from .models import Notification, Apartment, Booking

@login_required
def notifications_list(request):
    """عرض قائمة التنبيهات للمستخدم الحالي"""
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    
    # تحديث حالة التنبيهات لتكون مقروءة
    unread_notifications = notifications.filter(is_read=False)
    for notification in unread_notifications:
        notification.is_read = True
        notification.save()
    
    context = {
        'notifications': notifications
    }
    return render(request, 'apartments/notifications.html', context)

@login_required
def mark_notification_as_read(request, pk):
    """تحديد تنبيه كمقروء"""
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.is_read = True
    notification.save()
    
    # إعادة التوجيه حسب نوع التنبيه
    if notification.related_booking:
        if request.user == notification.related_booking.apartment.owner:
            return redirect('manage_bookings')
        else:
            return redirect('my_bookings')
    elif notification.related_apartment:
        return redirect('apartment_detail', pk=notification.related_apartment.pk)
    
    return redirect('notifications_list')

@login_required
def delete_notification(request, pk):
    """حذف تنبيه"""
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.delete()
    messages.success(request, 'تم حذف التنبيه بنجاح')
    return redirect('notifications_list')

@login_required
def mark_all_read(request):
    """تعليم جميع التنبيهات كمقروءة"""
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    messages.success(request, 'تم تعليم جميع التنبيهات كمقروءة')
    
    # العودة إلى الصفحة السابقة
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return HttpResponseRedirect(referer)
    return redirect('home')

@login_required
def get_notifications_count(request):
    """الحصول على عدد الإشعارات غير المقروءة (API)"""
    count = Notification.objects.filter(user=request.user, is_read=False).count()
    return JsonResponse({'count': count})

@login_required
@require_POST
def mark_notification_as_read_api(request, pk):
    """تعليم إشعار كمقروء عبر API"""
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.is_read = True
    notification.save()
    return JsonResponse({'success': True})

@login_required
def get_recent_notifications(request):
    """الحصول على آخر الإشعارات (API)"""
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:5]
    data = [{
        'id': notification.id,
        'message': notification.message,
        'type': notification.notification_type,
        'type_display': notification.get_notification_type_display(),
        'is_read': notification.is_read,
        'created_at': notification.created_at.strftime('%Y-%m-%d %H:%M'),
        'url': get_notification_url(notification)
    } for notification in notifications]
    
    return JsonResponse({'notifications': data})

def get_notification_url(notification):
    """الحصول على رابط الإشعار بناءً على نوعه"""
    if notification.related_booking:
        if notification.user == notification.related_booking.apartment.owner:
            return f"/apartments/manage-bookings/"
        else:
            return f"/apartments/my-bookings/"
    elif notification.related_apartment:
        return f"/apartments/{notification.related_apartment.pk}/"
    
    return "/apartments/notifications/"