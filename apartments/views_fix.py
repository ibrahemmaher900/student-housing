from django.shortcuts import render
from .models import Apartment, University
from django.db.models import Count, Avg, Sum, Q

def fix_nan_in_stats(context):
    """معالجة قيم NaN في الإحصائيات"""
    if 'stats' in context:
        stats = context['stats']
        # استبدال قيم NaN بصفر أو قيمة افتراضية
        if 'available_apartments' in stats and (stats['available_apartments'] is None or str(stats['available_apartments']) == 'nan'):
            stats['available_apartments'] = 0
        if 'total_apartments' in stats and (stats['total_apartments'] is None or str(stats['total_apartments']) == 'nan'):
            stats['total_apartments'] = 0
        if 'avg_price' in stats and (stats['avg_price'] is None or str(stats['avg_price']) == 'nan'):
            stats['avg_price'] = 0
    return context

# استيراد الدالة الأصلية وتعديلها
from apartments.views import home as original_home

def home_fixed(request):
    """نسخة معدلة من الصفحة الرئيسية تعالج قيم NaN"""
    response = original_home(request)
    if hasattr(response, 'context_data'):
        response.context_data = fix_nan_in_stats(response.context_data)
    return response
