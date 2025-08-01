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
    
    # فلترة البحث
    university = request.GET.get('university')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    apartment_type = request.GET.get('apartment_type')
    gender = request.GET.get('gender')
    furnished = request.GET.get('furnished')
    has_wifi = request.GET.get('has_wifi')
    has_ac = request.GET.get('has_ac')
    
    if university:
        apartments = apartments.filter(university_id=university)
    if min_price:
        apartments = apartments.filter(price__gte=min_price)
    if max_price:
        apartments = apartments.filter(price__lte=max_price)
    if apartment_type:
        apartments = apartments.filter(apartment_type=apartment_type)
    if gender:
        apartments = apartments.filter(gender=gender)
    if furnished:
        apartments = apartments.filter(furnished=True)
    if has_wifi:
        apartments = apartments.filter(has_wifi=True)
    if has_ac:
        apartments = apartments.filter(has_ac=True)
    
    paginator = Paginator(apartments, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'universities': universities,
        'wishlist_apartments': [],
        'filters': {
            'university': university,
            'min_price': min_price,
            'max_price': max_price,
            'apartment_type': apartment_type,
            'gender': gender,
            'furnished': furnished,
            'has_wifi': has_wifi,
            'has_ac': has_ac,
        }
    }
    return render(request, 'apartments/apartment_list.html', context)

def apartment_detail(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk)
    
    # زيادة عدد المشاهدات
    apartment.views_count += 1
    apartment.save(update_fields=['views_count'])
    
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
            
            # إنشاء تنبيه للمالك
            Notification.objects.create(
                user=apartment.owner,
                notification_type='booking_request',
                message=f'طلب حجز جديد من {request.user.username} لـ {apartment.title}',
                related_booking=booking,
                related_apartment=apartment
            )
            
            messages.success(request, 'تم إرسال طلب الحجز بنجاح')
            return redirect('apartment_detail', pk=apartment.pk)
    
    return redirect('apartment_detail', pk=apartment.pk)

@login_required
def add_apartment(request):
    if request.method == 'POST':
        try:
            apartment_type = request.POST.get('apartment_type', 'studio')
            
            apartment = Apartment(
                title=request.POST.get('title', 'شقة'),
                description=request.POST.get('description', ''),
                price=float(request.POST.get('price', 0) or 0),
                apartment_type=apartment_type,
                area=int(request.POST.get('area', 50) or 50),
                bedrooms=1,
                bathrooms=1,
                address=request.POST.get('address', ''),
                distance_to_university=float(request.POST.get('distance_to_university', 0) or 0),
                university_id=request.POST.get('university'),
                gender=request.POST.get('gender', 'all'),
                furnished=request.POST.get('furnished') == 'on',
                has_wifi=request.POST.get('has_wifi') == 'on',
                has_ac=request.POST.get('has_ac') == 'on',
                has_kitchen=request.POST.get('has_kitchen') == 'on',
                has_washer=request.POST.get('has_washer') == 'on',
                has_fridge=request.POST.get('has_fridge') == 'on',
                has_private_bathroom=request.POST.get('has_private_bathroom') == 'on',
                has_balcony=request.POST.get('has_balcony') == 'on',
                has_parking=request.POST.get('has_parking') == 'on',
                bills_included=request.POST.get('bills_included') == 'on',
                owner=request.user,
                status='pending'
            )
            
            # حفظ الإحداثيات
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            if latitude and longitude:
                try:
                    apartment.latitude = float(latitude)
                    apartment.longitude = float(longitude)
                except:
                    pass
            
            apartment.save()
            
            for image in request.FILES.getlist('images'):
                ApartmentImage.objects.create(apartment=apartment, image=image)
            
            # إنشاء تنبيه للمسؤولين
            from django.contrib.auth.models import User
            admins = User.objects.filter(is_staff=True)
            for admin in admins:
                Notification.objects.create(
                    user=admin,
                    notification_type='apartment_pending',
                    message=f'إعلان جديد يحتاج موافقة: {apartment.title}',
                    related_apartment=apartment
                )
            
            if apartment_type == 'room':
                messages.success(request, 'تم إضافة الغرفة!')
            elif apartment_type == 'bed':
                messages.success(request, 'تم إضافة السرير!')
            else:
                messages.success(request, 'تم إضافة الشقة!')
            
            return redirect('my_apartments')
        except Exception as e:
            messages.error(request, 'حدث خطأ في إضافة الإعلان')
    
    return render(request, 'apartments/add_apartment.html', {'universities': University.objects.all()})

@login_required
def edit_apartment(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk)
    
    if apartment.owner != request.user:
        messages.error(request, 'ليس لديك صلاحية تعديل هذه الشقة.')
        return redirect('apartment_detail', pk=apartment.pk)
    
    if request.method == 'POST':
        try:
            apartment.title = request.POST.get('title', apartment.title)
            apartment.description = request.POST.get('description', apartment.description)
            apartment.price = float(request.POST.get('price', apartment.price) or apartment.price)
            apartment.area = int(request.POST.get('area', apartment.area) or apartment.area)
            apartment.address = request.POST.get('address', apartment.address)
            apartment.distance_to_university = float(request.POST.get('distance_to_university', apartment.distance_to_university) or apartment.distance_to_university)
            apartment.university_id = request.POST.get('university') or apartment.university_id
            apartment.gender = request.POST.get('gender', apartment.gender)
            apartment.furnished = request.POST.get('furnished') == 'on'
            apartment.has_wifi = request.POST.get('has_wifi') == 'on'
            apartment.has_ac = request.POST.get('has_ac') == 'on'
            apartment.has_kitchen = request.POST.get('has_kitchen') == 'on'
            apartment.has_washer = request.POST.get('has_washer') == 'on'
            apartment.has_fridge = request.POST.get('has_fridge') == 'on'
            apartment.has_private_bathroom = request.POST.get('has_private_bathroom') == 'on'
            apartment.has_balcony = request.POST.get('has_balcony') == 'on'
            apartment.has_parking = request.POST.get('has_parking') == 'on'
            apartment.bills_included = request.POST.get('bills_included') == 'on'
            
            # تحديث الإحداثيات
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            if latitude and longitude:
                try:
                    apartment.latitude = float(latitude)
                    apartment.longitude = float(longitude)
                except:
                    pass
            
            apartment.save()
            
            # إضافة صور جديدة
            for image in request.FILES.getlist('images'):
                ApartmentImage.objects.create(apartment=apartment, image=image)
            
            messages.success(request, 'تم تحديث معلومات الشقة بنجاح!')
            return redirect('apartment_detail', pk=apartment.pk)
        except Exception as e:
            messages.error(request, 'حدث خطأ في تحديث الشقة')
    
    context = {
        'apartment': apartment,
        'universities': University.objects.all(),
    }
    return render(request, 'apartments/edit_apartment.html', context)

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
    apartments = Apartment.objects.filter(owner=request.user).order_by('-created_at')
    
    context = {
        'apartments': apartments,
        'pending_apartments': apartments.filter(status='pending'),
        'approved_apartments': apartments.filter(status='approved'),
        'rejected_apartments': apartments.filter(status='rejected'),
    }
    return render(request, 'apartments/my_apartments.html', context)

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(student=request.user).order_by('-created_at')
    
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
    bookings = Booking.objects.filter(apartment__owner=request.user).order_by('-created_at')
    return render(request, 'apartments/manage_bookings.html', {'bookings': bookings})

@login_required
def update_booking_status(request, pk, status):
    booking = get_object_or_404(Booking, pk=pk)
    
    if booking.apartment.owner != request.user:
        messages.error(request, 'ليس لديك صلاحية تحديث حالة هذا الحجز.')
        return redirect('manage_bookings')
    
    if status == 'approve':
        booking.status = 'approved'
        # إنشاء تنبيه للطالب
        Notification.objects.create(
            user=booking.student,
            notification_type='booking_approved',
            message=f'تمت الموافقة على طلب حجزك لـ {booking.apartment.title}',
            related_booking=booking,
            related_apartment=booking.apartment
        )
        messages.success(request, 'تمت الموافقة على الحجز بنجاح!')
    elif status == 'reject':
        booking.status = 'rejected'
        # إنشاء تنبيه للطالب
        Notification.objects.create(
            user=booking.student,
            notification_type='booking_rejected',
            message=f'تم رفض طلب حجزك لـ {booking.apartment.title}',
            related_booking=booking,
            related_apartment=booking.apartment
        )
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
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('apartment')
    return render(request, 'apartments/my_wishlist.html', {'wishlist_items': wishlist_items})

@login_required
def owner_dashboard(request):
    try:
        apartments = Apartment.objects.filter(owner=request.user)
        bookings = Booking.objects.filter(apartment__owner=request.user)
        notifications = Notification.objects.filter(user=request.user, is_read=False)[:5]
        
        context = {
            'apartments': apartments,
            'bookings': bookings,
            'notifications': notifications,
            'total_apartments': apartments.count(),
            'approved_apartments': apartments.filter(status='approved').count(),
            'pending_apartments': apartments.filter(status='pending').count(),
            'rejected_apartments': apartments.filter(status='rejected').count(),
            'pending_bookings': bookings.filter(status='pending').count(),
            'approved_bookings': bookings.filter(status='approved').count(),
            'total_bookings': bookings.count(),
            'total_views': sum(apt.views_count for apt in apartments),
        }
        return render(request, 'apartments/owner_dashboard.html', context)
    except:
        return render(request, 'apartments/owner_dashboard_simple.html', {'user': request.user})

@login_required
@user_passes_test(is_admin)
def admin_apartments(request):
    pending_apartments = Apartment.objects.filter(status='pending').order_by('-created_at')
    approved_apartments = Apartment.objects.filter(status='approved').order_by('-created_at')
    rejected_apartments = Apartment.objects.filter(status='rejected').order_by('-created_at')
    
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
    
    # إنشاء تنبيه للمالك
    Notification.objects.create(
        user=apartment.owner,
        notification_type='apartment_approved',
        message=f'تمت الموافقة على إعلانك: {apartment.title}',
        related_apartment=apartment
    )
    
    messages.success(request, 'تمت الموافقة على الشقة بنجاح!')
    return redirect('admin_apartments')

@login_required
@user_passes_test(is_admin)
def reject_apartment(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk)
    apartment.status = 'rejected'
    apartment.save()
    
    # إنشاء تنبيه للمالك
    Notification.objects.create(
        user=apartment.owner,
        notification_type='apartment_rejected',
        message=f'تم رفض إعلانك: {apartment.title}',
        related_apartment=apartment
    )
    
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

@login_required
def add_room(request):
    return redirect('add_apartment')

@login_required
def add_bed(request):
    return redirect('add_apartment')

def report_non_serious_booking(request, pk):
    return redirect('manage_bookings')