from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Apartment, Rating, Notification
from .forms import RatingForm

@login_required
def add_rating(request, apartment_id):
    apartment = get_object_or_404(Apartment, pk=apartment_id)
    
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.apartment = apartment
            rating.user = request.user
            rating.save()
            messages.success(request, 'تم إضافة التقييم بنجاح')
            return redirect('apartment_detail', pk=apartment_id)
    else:
        form = RatingForm()
    
    return render(request, 'apartments/add_rating.html', {'form': form, 'apartment': apartment})

@login_required
@require_POST
def delete_rating(request, rating_id):
    rating = get_object_or_404(Rating, pk=rating_id)
    if rating.user == request.user:
        apartment_id = rating.apartment.id
        rating.delete()
        messages.success(request, 'تم حذف التقييم')
    return redirect('apartment_detail', pk=apartment_id)

@login_required
@require_POST
def approve_rating(request, rating_id):
    if request.user.is_staff:
        rating = get_object_or_404(Rating, pk=rating_id)
        rating.is_approved = True
        rating.save()
        messages.success(request, 'تم اعتماد التقييم')
    return redirect('apartment_detail', pk=rating.apartment.id)

@login_required
@require_POST
def reject_rating(request, rating_id):
    if request.user.is_staff:
        rating = get_object_or_404(Rating, pk=rating_id)
        rating.is_approved = False
        rating.save()
        messages.success(request, 'تم رفض التقييم')
    return redirect('apartment_detail', pk=rating.apartment.id)