from .models import Notification

def notifications_processor(request):
    """إضافة التنبيهات وعددها إلى سياق القالب"""
    if request.user.is_authenticated:
        unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
        # الحصول على آخر 5 تنبيهات
        notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:5]
        
        # إضافة معلومات الحظر
        is_banned = False
        if hasattr(request.user, 'profile'):
            is_banned = request.user.profile.is_banned
        
        return {
            'unread_notifications_count': unread_count,
            'user_notifications': notifications,
            'is_user_banned': is_banned
        }
    return {
        'unread_notifications_count': 0,
        'user_notifications': [],
        'is_user_banned': False
    }