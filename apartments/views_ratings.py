from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.db.models import Avg
from .models import Apartment, Rating, Notification, Booking
from .forms import RatingForm

@login_required
def add_rating(request, apartment_id):
    """إضافة تقييم جديد للشقة"""
    apartment = get_object_or_404(Apartment, pk=apartment_id)
    
    # التحقق من أن المستخدم هو المستأجر الفعلي للشقة
    # البحث عن حجز معتمد ونشط (لم ينتهي بعد)
    active_booking = Booking.objects.filter(
        apartment=apartment,
        student=request.user,
        status='approved',
        end_date__gte=timezone.now().date()
    ).exists()
    
    # البحث عن حجز معتمد ومنتهي (سكن سابقاً)
    past_booking = Booking.objects.filter(
        apartment=apartment,
        student=request.user,
        status='approved',
        end_date__lt=timezone.now().date()
    ).exists()
    
    is_actual_tenant = active_booking or past_booking
    
    if not is_actual_tenant:
        messages.error(request, 'يمكن فقط للمستأجر الفعلي للشقة إضافة تقييم')
        return redirect('apartment_detail', pk=apartment_id)
    
    # التحقق من أن المستخدم لم يقم بتقييم الشقة من قبل
    existing_rating = Rating.objects.filter(apartment=apartment, user=request.user).first()
    
    if request.method == 'POST':
        if existing_rating:
            form = RatingForm(request.POST, instance=existing_rating)
            is_new = False
        else:
            form = RatingForm(request.POST)
            is_new = True
            
        if form.is_valid():
            rating = form.save(commit=False)
            if is_new:
                rating.apartment = apartment
                rating.user = request.user
            rating.save()
            
            # إنشاء إشعار لمالك الشقة
            if request.user != apartment.owner:
                action = 'إضافة' if is_new else 'تحديث'
                Notification.objects.create(
                    user=apartment.owner,
                    notification_type='new_comment',
                    message=f'قام {request.user.username} بـ{action} تقييم لشقتك {apartment.title}',
                    related_apartment=apartment
                )
            
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': 'تم حفظ تقييمك بنجاح'})
            
            messages.success(request, 'تم حفظ تقييمك بنجاح')
            return redirect('apartment_detail', pk=apartment_id)
    else:
        if existing_rating:
            form = RatingForm(instance=existing_rating)
        else:
            form = RatingForm()
    
    context = {
        'form': form,
        'apartment': apartment,
        'existing_rating': existing_rating
    }
    return render(request, 'apartments/add_rating.html', context)

@login_required
@require_POST
def delete_rating(request, rating_id):
    """حذف تقييم"""
    rating = get_object_or_404(Rating, pk=rating_id)
    
    # التحقق من أن المستخدم هو صاحب التقييم
    if rating.user != request.user:
        messages.error(request, 'لا يمكنك حذف هذا التقييم')
        return redirect('apartment_detail', pk=rating.apartment.id)
    
    apartment_id = rating.apartment.id
    rating.delete()
    messages.success(request, 'تم حذف التقييم بنجاح')
    return redirect('apartment_detail', pk=apartment_id)

@login_required
@require_POST
def approve_rating(request, rating_id):
    """اعتماد تقييم (للمسؤولين فقط)"""
    rating = get_object_or_404(Rating, pk=rating_id)
    
    # التحقق من أن المستخدم هو مسؤول
    if not request.user.is_staff:
        messages.error(request, 'ليس لديك صلاحية اعتماد هذا التقييم')
        return redirect('apartment_detail', pk=rating.apartment.id)
    
    rating.is_approved = True
    rating.save()
    
    # إنشاء إشعار لصاحب التقييم
    if request.user != rating.user:
        Notification.objects.create(
            user=rating.user,
            notification_type='new_comment',
            message=f'تمت الموافقة على تقييمك لشقة {rating.apartment.title}',
            related_apartment=rating.apartment
        )
    
    messages.success(request, 'تم اعتماد التقييم بنجاح')
    return redirect('apartment_detail', pk=rating.apartment.id)

@login_required
@require_POST
def reject_rating(request, rating_id):
    """رفض تقييم (للمسؤولين فقط)"""
    rating = get_object_or_404(Rating, pk=rating_id)
    
    # التحقق من أن المستخدم هو مسؤول
    if not request.user.is_staff:
        messages.error(request, 'ليس لديك صلاحية رفض هذا التقييم')
        return redirect('apartment_detail', pk=rating.apartment.id)
    
    rating.is_approved = False
    rating.save()
    
    # إنشاء إشعار لصاحب التقييم
    if request.user != rating.user:
        Notification.objects.create(
            user=rating.user,
            notification_type='new_comment',
            message=f'تم رفض تقييمك لشقة {rating.apartment.title}',
            related_apartment=rating.apartment
        )
    
    messages.success(request, 'تم رفض التقييم بنجاح')
    return redirect('apartment_detail', pk=rating.apartment.id)