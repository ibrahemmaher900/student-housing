from django.core.cache import cache
from django.db import connection
from django.conf import settings
import time

class PerformanceMiddleware:
    """Middleware لتحسين الأداء"""
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        
        response = self.get_response(request)
        
        # إضافة header لوقت الاستجابة
        duration = time.time() - start_time
        response['X-Response-Time'] = f'{duration:.3f}s'
        
        return response

class DatabaseOptimizationMiddleware:
    """تحسين استعلامات قاعدة البيانات"""
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        queries_before = len(connection.queries)
        
        response = self.get_response(request)
        
        queries_after = len(connection.queries)
        queries_count = queries_after - queries_before
        
        # إضافة عدد الاستعلامات للتطوير
        if settings.DEBUG:
            response['X-DB-Queries'] = str(queries_count)
        
        return response