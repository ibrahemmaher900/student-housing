from django import template
from apartments.models import Notification

register = template.Library()

@register.simple_tag
def get_unread_notifications_count(user):
    """حساب عدد التنبيهات غير المقروءة للمستخدم"""
    if user.is_authenticated:
        return Notification.objects.filter(user=user, is_read=False).count()
    return 0