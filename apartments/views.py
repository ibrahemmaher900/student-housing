from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.conf import settings
from django.utils import timezone
from .models import Apartment, ApartmentImage, Booking, University, Wishlist, Notification, Comment
from .forms import ApartmentForm, ApartmentImageForm, BookingForm, ApartmentSearchForm, CommentForm

def is_admin(user):
    return user.is_staff or user.is_superuser

def home(request):
    try:
        apartments = Apartment.objects.filter(status='approved')[:6]
        universities = University.objects.all()
        
        context = {
            'featured_apartments': apartments,
            'universities': universities,
            'apartments_count': apartments.count(),
            'universities_count': universities.count(),
            'users_count': 0,
            'bookings_count': 0,
            'students_count': 0,
            'owners_count': 0,
            'wishlist_apartments': [],
            'site_ratings': [],
        }
        return render(request, 'apartments/home.html', context)
    except:
        return render(request, 'apartments/home_simple.html')

def apartment_list(request):
    apartments = Apartment.objects.filter(status='approved')
    universities = University.objects.all()
    
    paginator = Paginator(apartments, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'universities': universities,
        'wishlist_apartments': [],
    }
    return render(request, 'apartments/apartment_list.html', context)

def apartment_detail(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk)
    
    context = {
        'apartment': apartment,
        'comments': [],
        'ratings': [],
        'user_has_booking': False,
        'is_in_wishlist': False,
        'user_has_rating': False,
        'user_has_active_booking_elsewhere': False,
        'has_approved_booking': False,
        'is_actual_tenant': False,
        'today': timezone.now().date(),
    }
    return render(request, 'apartments/apartment_detail.html', context)

@login_required
def book_apartment(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk)
    
    if request.user == apartment.owner:
        messages.error(request, 'لا يمكنك حجز شقتك الخاصة!')
        return redirect('apartment_detail', pk=apartment.pk)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.apartment = apartment
            booking.student = request.user
            booking.save()
            messages.success(request, 'تم إرسال طلب الحجز بنجاح')
            return redirect('apartment_detail', pk=apartment.pk)
    
    return redirect('apartment_detail', pk=apartment.pk)

@login_required
def add_apartment(request):
    if request.method == 'POST':
        apartment = Apartment(
            title=request.POST.get('title', 'شقة'),
            description=request.POST.get('description', ''),
            price=request.POST.get('price', 0),
            apartment_type='studio',
            area=request.POST.get('area', 50),
            bedrooms=1,
            bathrooms=1,
            address=request.POST.get('address', ''),
            distance_to_university=request.POST.get('distance_to_university', 0),
            university_id=request.POST.get('university'),
            owner=request.user,
            status='pending'
        )
        apartment.save()
        
        for image in request.FILES.getlist('images'):
            ApartmentImage.objects.create(apartment=apartment, image=image)
        
        messages.success(request, 'تم إضافة الشقة!')
        return redirect('my_apartments')
    
    return render(request, 'apartments/add_apartment_simple.html', {'universities': University.objects.all()})

@login_required
def edit_apartment(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk)
    
    if apartment.owner != request.user:
        messages.error(request, 'ليس لديك صلاحية تعديل هذه الشقة.')
        return redirect('apartment_detail', pk=apartment.pk)
    
    if request.method == 'POST':
        form = ApartmentForm(request.POST, instance=apartment)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تحديث معلومات الشقة بنجاح!')
            return redirect('apartment_detail', pk=apartment.pk)
    else:
        form = ApartmentForm(instance=apartment)
    
    return render(request, 'apartments/edit_apartment.html', {'form': form, 'apartment': apartment})

@login_required
def delete_apartment(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk)
    
    if apartment.owner != request.user:
        messages.error(request, 'ليس لديك صلاحية حذف هذه الشقة.')
        return redirect('apartment_detail', pk=apartment.pk)
    
    if request.method == 'POST':
        apartment.delete()
        messages.success(request, 'تم حذف الشقة بنجاح!')
        return redirect('my_apartments')
    
    return render(request, 'apartments/delete_apartment.html', {'apartment': apartment})

@login_required
def my_apartments(request):
    apartments = Apartment.objects.filter(owner=request.user)
    
    context = {
        'apartments': apartments,
        'pending_apartments': apartments.filter(status='pending'),
        'approved_apartments': apartments.filter(status='approved'),
        'rejected_apartments': apartments.filter(status='rejected'),
    }
    return render(request, 'apartments/my_apartments.html', context)

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(student=request.user)
    
    context = {
        'bookings': bookings,
        'pending_bookings': bookings.filter(status='pending'),
        'approved_bookings': bookings.filter(status='approved'),
        'rejected_bookings': bookings.filter(status='rejected'),
        'active_bookings': [],
        'past_bookings': [],
    }
    return render(request, 'apartments/my_bookings.html', context)

@login_required
def manage_bookings(request):
    bookings = Booking.objects.filter(apartment__owner=request.user)
    return render(request, 'apartments/manage_bookings.html', {'bookings': bookings})

@login_required
def update_booking_status(request, pk, status):
    booking = get_object_or_404(Booking, pk=pk)
    
    if booking.apartment.owner != request.user:
        messages.error(request, 'ليس لديك صلاحية تحديث حالة هذا الحجز.')
        return redirect('manage_bookings')
    
    if status == 'approve':
        booking.status = 'approved'
        messages.success(request, 'تمت الموافقة على الحجز بنجاح!')
    elif status == 'reject':
        booking.status = 'rejected'
        messages.success(request, 'تم رفض الحجز بنجاح!')
    
    booking.save()
    return redirect('manage_bookings')

@login_required
def toggle_wishlist(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk)
    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,
        apartment=apartment
    )
    
    if not created:
        wishlist_item.delete()
        message = 'تمت إزالة الشقة من المفضلات'
    else:
        message = 'تمت إضافة الشقة إلى المفضلات'
    
    messages.success(request, message)
    return redirect('apartment_detail', pk=apartment.pk)

@login_required
def my_wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'apartments/my_wishlist.html', {'wishlist_items': wishlist_items})

@login_required
def owner_dashboard(request):
    try:
        apartments = Apartment.objects.filter(owner=request.user)
        bookings = Booking.objects.filter(apartment__owner=request.user)
        
        context = {
            'apartments': apartments,
            'bookings': bookings,
            'total_apartments': apartments.count(),
            'approved_apartments': apartments.filter(status='approved').count(),
            'pending_bookings': bookings.filter(status='pending').count(),
            'total_bookings': bookings.count(),
        }
        return render(request, 'apartments/owner_dashboard.html', context)
    except:
        return render(request, 'apartments/owner_dashboard_simple.html', {'user': request.user})

@login_required
@user_passes_test(is_admin)
def admin_apartments(request):
    pending_apartments = Apartment.objects.filter(status='pending')
    approved_apartments = Apartment.objects.filter(status='approved')
    rejected_apartments = Apartment.objects.filter(status='rejected')
    
    context = {
        'pending_apartments': pending_apartments,
        'approved_apartments': approved_apartments,
        'rejected_apartments': rejected_apartments,
    }
    return render(request, 'apartments/admin_apartments.html', context)

@login_required
@user_passes_test(is_admin)
def approve_apartment(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk)
    apartment.status = 'approved'
    apartment.save()
    messages.success(request, 'تمت الموافقة على الشقة بنجاح!')
    return redirect('admin_apartments')

@login_required
@user_passes_test(is_admin)
def reject_apartment(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk)
    apartment.status = 'rejected'
    apartment.save()
    messages.success(request, 'تم رفض الشقة بنجاح!')
    return redirect('admin_apartments')

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    from django.contrib.auth.models import User
    
    context = {
        'total_users': User.objects.count(),
        'total_apartments': Apartment.objects.count(),
        'pending_apartments': Apartment.objects.filter(status='pending').count(),
        'total_bookings': Booking.objects.count(),
        'students_count': 0,
        'owners_count': 0,
        'recent_students': [],
        'recent_owners': [],
        'approved_apartments': Apartment.objects.filter(status='approved').count(),
        'rejected_apartments': Apartment.objects.filter(status='rejected').count(),
        'pending_apartments_list': Apartment.objects.filter(status='pending')[:10],
        'approved_bookings': Booking.objects.filter(status='approved').count(),
        'pending_bookings': Booking.objects.filter(status='pending').count(),
        'rejected_bookings': Booking.objects.filter(status='rejected').count(),
        'recent_bookings': Booking.objects.all()[:10],
    }
    return render(request, 'apartments/admin_dashboard.html', context)

def report_non_serious_booking(request, pk):
    return redirect('manage_bookings')