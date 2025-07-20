from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseForbidden
import re

class SecurityMiddleware(MiddlewareMixin):
    """
    وسيط أمان مخصص لتعزيز أمان التطبيق
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # تعريف أنماط الطلبات المشبوهة
        self.sql_injection_pattern = re.compile(r'(\b(select|update|delete|insert|drop|alter|union|into|load_file)\b)', re.IGNORECASE)
        self.xss_pattern = re.compile(r'(<script|javascript:|on\w+\s*=)', re.IGNORECASE)
        self.path_traversal_pattern = re.compile(r'(\.\./|\.\.\\)')
        
    def process_request(self, request):
        # فحص محتوى الطلب بحثًا عن محاولات اختراق
        if self._check_malicious_content(request):
            return HttpResponseForbidden("طلب محظور: تم اكتشاف محتوى مشبوه")
        return None
    
    def _check_malicious_content(self, request):
        """فحص محتوى الطلب بحثًا عن أنماط هجوم معروفة"""
        # فحص معلمات GET
        for key, value in request.GET.items():
            if isinstance(value, str):
                if (self.sql_injection_pattern.search(value) or 
                    self.xss_pattern.search(value) or 
                    self.path_traversal_pattern.search(value)):
                    return True
        
        # فحص معلمات POST
        for key, value in request.POST.items():
            if isinstance(value, str):
                if (self.sql_injection_pattern.search(value) or 
                    self.xss_pattern.search(value) or 
                    self.path_traversal_pattern.search(value)):
                    return True
        
        # فحص مسار URL
        if (self.sql_injection_pattern.search(request.path) or 
            self.xss_pattern.search(request.path) or 
            self.path_traversal_pattern.search(request.path)):
            return True
            
        return False