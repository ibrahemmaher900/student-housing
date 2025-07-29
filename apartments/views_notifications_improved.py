from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from .models import Notification

@login_required
def notifications_list(request):
    notifications = Notification.objects.filter(user=request.user).select_related(
        'related_apartment', 'related_booking', 'related_comment'
    ).order_by('-created_at')
    
    # فلترة حسب النوع
    filter_type = request.GET.get('type')
    if filter_type:
        notifications = notifications.filter(notification_type=filter_type)
    
    # فلترة حسب الحالة
    filter_status = request.GET.get('status')
    if filter_status == 'unread':
        notifications = notifications.filter(is_read=False)
    elif filter_status == 'read':
        notifications = notifications.filter(is_read=True)
    
    paginator = Paginator(notifications, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'filter_type': filter_type,
        'filter_status': filter_status,
        'unread_count': Notification.objects.filter(user=request.user, is_read=False).count()
    }
    return render(request, 'apartments/notifications.html', context)

@login_required
def mark_notification_as_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.is_read = True
    notification.save(update_fields=['is_read'])
    
    if notification.related_apartment:
        return redirect('apartment_detail', pk=notification.related_apartment.pk)
    elif notification.related_booking:
        if request.user.profile.user_type == 'owner':
            return redirect('manage_bookings')
        else:
            return redirect('my_bookings')
    return redirect('notifications_list')

@login_required
def delete_notification(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.delete()
    return JsonResponse({'success': True, 'message': 'تم حذف التنبيه'})

@login_required
@require_POST
def mark_all_read(request):
    updated = Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return JsonResponse({'success': True, 'updated_count': updated})

@login_required
@require_POST
def delete_all_read(request):
    deleted = Notification.objects.filter(user=request.user, is_read=True).delete()[0]
    return JsonResponse({'success': True, 'deleted_count': deleted})

@login_required
def get_notifications_count(request):
    count = Notification.objects.filter(user=request.user, is_read=False).count()
    return JsonResponse({'count': count})

@login_required
@require_POST
def mark_notification_as_read_api(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.is_read = True
    notification.save(update_fields=['is_read'])
    return JsonResponse({'success': True})

@login_required
def get_recent_notifications(request):
    notifications = Notification.objects.filter(user=request.user).select_related(
        'related_apartment', 'related_booking'
    ).order_by('-created_at')[:15]
    
    notifications_data = []
    for notification in notifications:
        data = {
            'id': notification.id,
            'message': notification.message,
            'is_read': notification.is_read,
            'created_at': notification.created_at.isoformat(),
            'type': notification.notification_type,
            'url': get_notification_url(notification)
        }
        notifications_data.append(data)
    
    unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
    
    return JsonResponse({
        'notifications': notifications_data,
        'unread_count': unread_count
    })

def get_notification_url(notification):
    """إرجاع الرابط المناسب للتنبيه"""
    if notification.related_apartment:
        return f'/apartments/{notification.related_apartment.pk}/'
    elif notification.related_booking:
        if notification.user.profile.user_type == 'owner':
            return '/apartments/manage-bookings/'
        else:
            return '/apartments/my-bookings/'
    return '/notifications/'

# دالة مساعدة لإنشاء التنبيهات
def create_notification(user, notification_type, message, related_apartment=None, related_booking=None, related_comment=None):
    """دالة محسنة لإنشاء التنبيهات"""
    try:
        # تجنب التنبيهات المكررة
        if related_booking:
            existing = Notification.objects.filter(
                user=user,
                notification_type=notification_type,
                related_booking=related_booking,
                created_at__gte=timezone.now() - timedelta(minutes=5)
            ).exists()
            if existing:
                return None
        
        notification = Notification.objects.create(
            user=user,
            notification_type=notification_type,
            message=message,
            related_apartment=related_apartment,
            related_booking=related_booking,
            related_comment=related_comment
        )
        return notification
    except Exception:
        return None

# تنظيف التنبيهات القديمة
@login_required
@require_POST
def cleanup_old_notifications(request):
    """حذف التنبيهات القديمة (أكثر من 30 يوم)"""
    if request.user.is_staff:
        old_date = timezone.now() - timedelta(days=30)
        deleted = Notification.objects.filter(
            created_at__lt=old_date,
            is_read=True
        ).delete()[0]
        return JsonResponse({'success': True, 'deleted_count': deleted})
    return JsonResponse({'success': False, 'error': 'غير مسموح'})