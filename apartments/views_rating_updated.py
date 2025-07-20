from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import json
from .models import SiteRating

@login_required
@require_POST
def submit_rating(request):
    """وظيفة لاستقبال تقييمات الموقع"""
    try:
        data = json.loads(request.body)
        rating = data.get('rating')
        review = data.get('review', '')
        
        # التحقق من صحة البيانات
        if not rating or not rating.isdigit() or int(rating) < 1 or int(rating) > 5:
            return JsonResponse({'status': 'error', 'message': 'التقييم غير صالح'})
        
        # حفظ التقييم وتعيينه كمعتمد تلقائيًا
        site_rating = SiteRating(
            user=request.user,
            rating=int(rating),
            review=review,
            is_approved=True
        )
        site_rating.save()
        
        return JsonResponse({'status': 'success', 'message': 'تم حفظ التقييم بنجاح'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})