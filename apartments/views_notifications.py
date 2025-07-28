from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Notification

@login_required
def notifications_list(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'apartments/notifications.html', {'notifications': notifications})

@login_required
def mark_notification_as_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.is_read = True
    notification.save()

    # توجيه حسب نوع الإشعار
    if notification.related_apartment:
        return redirect('apartment_detail', pk=notification.related_apartment.pk)
    elif notification.related_booking:
        # توجيه حسب نوع المستخدم
        if hasattr(request.user, 'profile') and getattr(request.user.profile, 'user_type', None) == 'owner':
            return redirect('manage_bookings')
        else:
            return redirect('my_bookings')
    elif notification.related_comment:
        # توجيه لتعليق (صفحة الشقة مع تمرير التعليق)
        return redirect('apartment_detail', pk=notification.related_comment.apartment.pk)
    # يمكن إضافة أنواع أخرى لاحقاً
    return redirect('notifications_list')

@login_required
def delete_notification(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.delete()
    messages.success(request, 'تم حذف التنبيه')
    return redirect('notifications_list')

@login_required
@require_POST
def mark_all_read(request):
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return JsonResponse({'success': True})

@login_required
def get_notifications_count(request):
    count = Notification.objects.filter(user=request.user, is_read=False).count()
    return JsonResponse({'count': count})

@login_required
@require_POST
def mark_notification_as_read_api(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.is_read = True
    notification.save()

    # تحديد الرابط المناسب
    url = None
    if notification.related_apartment:
        from django.urls import reverse
        url = reverse('apartment_detail', kwargs={'pk': notification.related_apartment.pk})
    elif notification.related_booking:
        from django.urls import reverse
        if hasattr(request.user, 'profile') and getattr(request.user.profile, 'user_type', None) == 'owner':
            url = reverse('manage_bookings')
        else:
            url = reverse('my_bookings')
    elif notification.related_comment:
        from django.urls import reverse
        url = reverse('apartment_detail', kwargs={'pk': notification.related_comment.apartment.pk})
    # يمكن إضافة أنواع أخرى لاحقاً
    return JsonResponse({'success': True, 'redirect_url': url})

@login_required
def get_recent_notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:10]
    
    notifications_data = []
    for notification in notifications:
        data = {
            'id': notification.id,
            'message': notification.message,
            'is_read': notification.is_read,
            'created_at': notification.created_at.isoformat(),
        }
        notifications_data.append(data)
    
    unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
    
    return JsonResponse({
        'notifications': notifications_data,
        'unread_count': unread_count
    })