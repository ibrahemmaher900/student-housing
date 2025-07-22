from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import SiteRating

@ensure_csrf_cookie
@login_required
def simple_rating(request):
    """وظيفة بسيطة لإضافة تقييم"""
    if request.method == 'POST':
        try:
            rating = request.POST.get('rating')
            comment = request.POST.get('comment', '')
            
            # التحقق من البيانات
            if not rating:
                return JsonResponse({'status': 'error', 'message': 'التقييم مطلوب'})
            
            # إنشاء التقييم
            SiteRating.objects.create(
                user=request.user,
                rating=int(rating),
                comment=comment
            )
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'message': 'تم إضافة التقييم بنجاح'})
            else:
                return redirect('home')
        except Exception as e:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'message': str(e)})
            else:
                return render(request, 'apartments/simple_rating.html', {'error': str(e)})
    
    return render(request, 'apartments/simple_rating.html')
