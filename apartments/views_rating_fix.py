from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import SiteRating
import logging
import json

logger = logging.getLogger(__name__)

@ensure_csrf_cookie
@login_required
def add_rating(request):
    """إضافة تقييم للموقع"""
    if request.method == 'POST':
        try:
            rating = request.POST.get('rating')
            comment = request.POST.get('comment', '')
            
            # تسجيل البيانات للتصحيح
            logger.info(f"Adding rating: {rating}, comment: {comment}")
            
            # التحقق من البيانات
            if not rating:
                return JsonResponse({'status': 'error', 'message': 'التقييم مطلوب'})
            
            # إنشاء التقييم
            SiteRating.objects.create(
                user=request.user,
                rating=int(rating),
                comment=comment
            )
            
            return JsonResponse({'status': 'success', 'message': 'تم إضافة التقييم بنجاح'})
        except Exception as e:
            logger.error(f"Error adding rating: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return render(request, 'apartments/add_rating.html')
