from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.contrib import messages
import logging

logger = logging.getLogger('student_housing.security_middleware')

class BannedUserMiddleware:
    """Middleware لمنع المستخدمين المحظورين من الوصول"""
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # التحقق من حظر المستخدم
        if request.user.is_authenticated:
            try:
                if hasattr(request.user, 'profile') and request.user.profile.is_banned:
                    # السماح بالوصول لصفحات معينة فقط
                    allowed_paths = [
                        '/users/logout/',
                        '/users/profile/',
                        '/apartments/notifications/',
                    ]
                    
                    if not any(request.path.startswith(path) for path in allowed_paths):
                        messages.error(request, 'تم تجميد حسابك بسبب تكرار عدم الجدية في الحجز. يرجى التواصل مع إدارة الموقع.')
                        return redirect('profile')
            except:
                pass

        response = self.get_response(request)
        return response

class SecurityHeadersMiddleware:
    """Middleware لإضافة headers الأمان"""
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # إضافة headers الأمان
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        return response