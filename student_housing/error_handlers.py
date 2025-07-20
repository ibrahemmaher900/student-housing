from django.shortcuts import render
from django.views.defaults import page_not_found, server_error, permission_denied
import logging

logger = logging.getLogger(__name__)

def handler404(request, exception):
    """
    معالج مخصص لخطأ 404 (الصفحة غير موجودة)
    """
    return page_not_found(request, exception, template_name='errors/404.html')

def handler500(request):
    """
    معالج مخصص لخطأ 500 (خطأ في الخادم)
    """
    # تسجيل الخطأ
    logger.error('حدث خطأ 500 في الخادم', exc_info=True, extra={
        'request': request,
    })
    return server_error(request, template_name='errors/500.html')

def handler403(request, exception):
    """
    معالج مخصص لخطأ 403 (الوصول محظور)
    """
    return permission_denied(request, exception, template_name='errors/403.html')

def handler400(request, exception):
    """
    معالج مخصص لخطأ 400 (طلب غير صالح)
    """
    return render(request, 'errors/400.html', status=400)