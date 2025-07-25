from django.http import HttpResponseForbidden, Http404
from django.shortcuts import render
from django.conf import settings
import re
import logging

logger = logging.getLogger(__name__)

class SecurityMiddleware:
    """Middleware للحماية الأمنية الشاملة"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        
        # قائمة المسارات المحظورة
        self.forbidden_paths = [
            r'\.git',
            r'\.env',
            r'__pycache__',
            r'\.pyc$',
            r'\.pyo$',
            r'\.py$',
            r'migrations/',
            r'\.sqlite',
            r'\.db$',
            r'\.log$',
            r'\.ini$',
            r'\.conf$',
            r'venv/',
            r'env/',
            r'node_modules/',
            r'\.vscode/',
            r'\.idea/',
            r'requirements\.txt$',
            r'manage\.py$',
            r'wsgi\.py$',
            r'settings\.py$',
        ]
        
        # أنماط الهجمات المشبوهة
        self.suspicious_patterns = [
            r'union.*select',
            r'drop.*table',
            r'insert.*into',
            r'delete.*from',
            r'update.*set',
            r'<script',
            r'javascript:',
            r'onload=',
            r'onerror=',
            r'\.\./',
            r'etc/passwd',
            r'proc/self',
            r'cmd\.exe',
            r'powershell',
        ]

    def __call__(self, request):
        # فحص المسار المطلوب
        path = request.path.lower()
        
        # التحقق من المسارات المحظورة
        for pattern in self.forbidden_paths:
            if re.search(pattern, path, re.IGNORECASE):
                logger.warning(f"Blocked access to forbidden path: {request.path} from IP: {self.get_client_ip(request)}")
                raise Http404("الصفحة غير موجودة")
        
        # فحص المعاملات للهجمات المشبوهة
        query_string = request.META.get('QUERY_STRING', '').lower()
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        
        for pattern in self.suspicious_patterns:
            if re.search(pattern, query_string, re.IGNORECASE) or re.search(pattern, user_agent, re.IGNORECASE):
                logger.critical(f"Suspicious activity detected: {pattern} from IP: {self.get_client_ip(request)}")
                return HttpResponseForbidden("طلب مشبوه - تم حظر الوصول")
        
        # فحص حجم الطلب
        if request.META.get('CONTENT_LENGTH'):
            try:
                content_length = int(request.META['CONTENT_LENGTH'])
                if content_length > 50 * 1024 * 1024:  # 50MB
                    logger.warning(f"Large request blocked: {content_length} bytes from IP: {self.get_client_ip(request)}")
                    return HttpResponseForbidden("حجم الطلب كبير جداً")
            except ValueError:
                pass
        
        # فحص معدل الطلبات (Rate Limiting بسيط)
        if not self.check_rate_limit(request):
            logger.warning(f"Rate limit exceeded from IP: {self.get_client_ip(request)}")
            return HttpResponseForbidden("تم تجاوز الحد المسموح من الطلبات")
        
        response = self.get_response(request)
        
        # إضافة headers الأمان
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        return response
    
    def get_client_ip(self, request):
        """الحصول على IP الحقيقي للعميل"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def check_rate_limit(self, request):
        """فحص معدل الطلبات (تنفيذ بسيط)"""
        # يمكن تحسينه باستخدام Redis أو cache
        return True  # مؤقتاً نسمح بجميع الطلبات