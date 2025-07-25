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
import json

# دالة للتحقق من أن المستخدم مسؤول
def is_admin(user):
    return user.is_staff or user.is_superuser

def home(request):
    from django.contrib.auth.models import User
    from django.db.models import Count
    from django.core.cache import cache
    from .models import SiteRating
    
    # استخدام التخزين المؤقت للبيانات الثابتة
    cache_key = 'home_page_data'
    cached_data = cache.get(cache_key)
    
    if cached_data:
        return render(request, 'apartments/home.html', cached_data)
    
    # الشقق المميزة
    featured_apartments = Apartment.objects.select_related('university', 'owner').prefetch_related('images').filter(available=True, status='approved').order_by('-created_at')[:6]
    
    # إضافة معلومات الحجز المعتمد لكل شقة
    for apartment in featured_apartments:
        apartment.has_approved_booking = apartment.has_approved_booking()
        if apartment.has_approved_booking:
            approved_booking = apartment.get_approved_booking()
            if approved_booking:
                apartment.approved_booking_start = approved_booking.start_date
                apartment.approved_booking_end = approved_booking.end_date
    
    # الجامعات
    universities = University.objects.all()
    
    # إحصائيات المنصة
    apartments_count = Apartment.objects.filter(status='approved').count()
    universities_count = universities.count()
    users_count = User.objects.count()
    bookings_count = Booking.objects.filter(status='approved').count()
    
    # إحصائيات إضافية
    try:
        students_count = User.objects.filter(profile__user_type='student').count()
        owners_count = User.objects.filter(profile__user_type='owner').count()
    except:
        students_count = 0
        owners_count = 0
    
    # الحصول على قائمة المفضلات للمستخدم الحالي
    wishlist_apartments = []
    if request.user.is_authenticated:
        wishlist_apartments = Wishlist.objects.filter(user=request.user).values_list('apartment_id', flat=True)
    
    # الحصول على تقييمات الموقع المعتمدة
    site_ratings = []
    
    context = {
        'featured_apartments': featured_apartments,
        'universities': universities,
        'apartments_count': apartments_count,
        'universities_count': universities_count,
        'users_count': users_count,
        'bookings_count': bookings_count,
        'students_count': students_count,
        'owners_count': owners_count,
        'wishlist_apartments': wishlist_apartments,
        'site_ratings': site_ratings,
    }
    
    # حفظ في التخزين المؤقت لمدة 5 دقائق
    cache.set(cache_key, context, 300)
    
    return render(request, 'apartments/home.html', context)

def apartment_list(request):
    apartments = Apartment.objects.select_related('university', 'owner').prefetch_related('images').filter(available=True, status='approved')
    universities = University.objects.all().only('id', 'name')
    
    # فلترة البحث
    university = request.GET.get('university')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    apartment_type = request.GET.get('apartment_type')
    bedrooms = request.GET.get('bedrooms')
    furnished = request.GET.get('furnished')
    has_wifi = request.GET.get('has_wifi')
    has_ac = request.GET.get('has_ac')
    
    if university:
        apartments = apartments.filter(university_id=university)
    if min_price:
        try:
            apartments = apartments.filter(price__gte=float(min_price))
        except ValueError:
            pass
    if max_price:
        try:
            apartments = apartments.filter(price__lte=float(max_price))
        except ValueError:
            pass
    if apartment_type:
        apartments = apartments.filter(apartment_type=apartment_type)
    if bedrooms:
        try:
            apartments = apartments.filter(bedrooms__gte=int(bedrooms))
        except ValueError:
            pass
    if furnished:
        apartments = apartments.filter(furnished=True)
    if has_wifi:
        apartments = apartments.filter(has_wifi=True)
    if has_ac:
        apartments = apartments.filter(has_ac=True)
    
    # الترتيب
    sort_param = request.GET.get('sort')
    if sort_param == 'price_asc':
        apartments = apartments.order_by('price')
    elif sort_param == 'price_desc':
        apartments = apartments.order_by('-price')
    elif sort_param == 'newest':
        apartments = apartments.order_by('-created_at')
    else:
        apartments = apartments.order_by('-created_at')  # الترتيب الافتراضي
    
    # الحصول على قائمة المفضلات للمستخدم الحالي
    wishlist_apartments = []
    if request.user.is_authenticated:
        wishlist_apartments = Wishlist.objects.filter(user=request.user).values_list('apartment_id', flat=True)
    
    paginator = Paginator(apartments, 9)  # 9 شقق في كل صفحة
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # إضافة معلومات الحجز المعتمد لكل شقة
    for apartment in page_obj:
        apartment.has_approved_booking = apartment.has_approved_booking()
    
    context = {
        'page_obj': page_obj,
        'universities': universities,
        'wishlist_apartments': wishlist_apartments,
    }
    return render(request, 'apartments/apartment_list.html', context)

def apartment_detail(request, pk):
    """عرض تفاصيل الشقة"""
    apartment = get_object_or_404(Apartment, pk=pk)
    
    # زيادة عدد المشاهدات
    apartment.views_count += 1
    apartment.save(update_fields=['views_count'])
    
    # الحصول على التعليقات والردود عليها
    comments = Comment.objects.filter(apartment=apartment).order_by('-created_at')
    
    # الحصول على التقييمات
    ratings = apartment.ratings.filter(is_approved=True).order_by('-created_at')
    
    # التحقق مما إذا كان المستخدم قد قام بالحجز من قبل
    user_has_booking = False
    is_in_wishlist = False
    user_has_rating = False
    user_has_active_booking_elsewhere = False
    is_actual_tenant = False
    
    if request.user.is_authenticated:
        # التحقق من حجز المستخدم لهذه الشقة
        user_booking = Booking.objects.filter(
            apartment=apartment,
            student=request.user
        ).first()
        
        if user_booking:
            user_has_booking = True
            user_booking_status = user_booking.status
        else:
            user_has_booking = False
            user_booking_status = None
        
        # التحقق من أن المستخدم هو المستأجر الفعلي للشقة (حجز معتمد حالي أو سابق)
        active_booking = Booking.objects.filter(
            apartment=apartment,
            student=request.user,
            status='approved',
            end_date__gte=timezone.now().date()
        ).exists()
        
        past_booking = Booking.objects.filter(
            apartment=apartment,
            student=request.user,
            status='approved',
            end_date__lt=timezone.now().date()
        ).exists()
        
        is_actual_tenant = active_booking or past_booking
        
        # التحقق من وجود حجز نشط في شقة أخرى
        user_has_active_booking_elsewhere = Booking.objects.filter(
            student=request.user,
            status__in=['pending', 'approved'],
            end_date__gte=timezone.now().date()
        ).exclude(apartment=apartment).exists()
        
        # التحقق مما إذا كانت الشقة في المفضلات
        is_in_wishlist = Wishlist.objects.filter(
            apartment=apartment,
            user=request.user
        ).exists()
        
        # التحقق مما إذا كان المستخدم قد قام بتقييم الشقة من قبل
        user_has_rating = apartment.ratings.filter(user=request.user).exists()
    
    # الحصول على معلومات الحجز المعتمد
    has_approved_booking = apartment.has_approved_booking()
    approved_booking_start = None
    approved_booking_end = None
    
    if has_approved_booking:
        approved_booking = apartment.get_approved_booking()
        if approved_booking:
            approved_booking_start = approved_booking.start_date
            approved_booking_end = approved_booking.end_date
    
    context = {
        'apartment': apartment,
        'comments': comments,
        'ratings': ratings,
        'user_has_booking': user_has_booking,
        'user_booking_status': user_booking_status,
        'is_in_wishlist': is_in_wishlist,
        'user_has_rating': user_has_rating,
        'user_has_active_booking_elsewhere': user_has_active_booking_elsewhere,
        'settings': settings,
        'has_approved_booking': has_approved_booking,
        'approved_booking_start': approved_booking_start,
        'approved_booking_end': approved_booking_end,
        'is_actual_tenant': is_actual_tenant,
        'today': timezone.now().date(),
    }
    return render(request, 'apartments/apartment_detail.html', context)

# تم إزالة الاسم المستعار لأننا نستخدم الآن قالب واحد فقط

@login_required
def book_apartment(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk)
    
    # التحقق من أن المستخدم ليس هو مالك الشقة
    if request.user == apartment.owner:
        messages.error(request, 'لا يمكنك حجز شقتك الخاصة!')
        return redirect('apartment_detail', pk=apartment.pk)
    
    # التحقق من أن المستخدم غير محظور
    if hasattr(request.user, 'profile') and request.user.profile.is_banned:
        messages.error(request, 'تم تجميد حسابك بسبب تكرار عدم الجدية في الحجز. يرجى التواصل مع إدارة الموقع.')
        return redirect('apartment_detail', pk=apartment.pk)
    
    # التحقق من أن المستخدم ليس لديه حجز نشط
    active_bookings = Booking.objects.filter(
        student=request.user,
        status__in=['pending', 'approved'],
        end_date__gte=timezone.now().date()
    )
    
    # التحقق من أن المستخدم ليس لديه حجز مرفوض حديثاً
    rejected_bookings = Booking.objects.filter(
        student=request.user,
        status='rejected'
    )
    
    if active_bookings.exists() and not rejected_bookings.exists():
        messages.error(request, 'لا يمكنك حجز أكثر من شقة في نفس الوقت. يرجى الانتظار حتى انتهاء فترة الإيجار الحالية أو رفض طلب الحجز الحالي.')
        return redirect('apartment_detail', pk=apartment.pk)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.apartment = apartment
            booking.student = request.user
            booking.save()
            
            # إنشاء تنبيه للمالك
            owner_notification = Notification(
                user=apartment.owner,
                notification_type='booking_request',
                message=f'قام {request.user.username} بطلب حجز شقتك {apartment.title}',
                related_booking=booking,
                related_apartment=apartment
            )
            owner_notification.save()
            
            # إنشاء تنبيه للمسؤولين
            from django.contrib.auth.models import User
            admins = User.objects.filter(is_staff=True) | User.objects.filter(is_superuser=True)
            for admin in admins:
                Notification.objects.create(
                    user=admin,
                    notification_type='booking_request',
                    message=f'طلب حجز جديد: قام {request.user.username} بطلب حجز شقة {apartment.title}',
                    related_booking=booking,
                    related_apartment=apartment
                )
            
            messages.success(request, 'تم إرسال طلب الحجز بنجاح. سيتم إعلامك عند الموافقة عليه.')
            return redirect('apartment_detail', pk=apartment.pk)
    
    return redirect('apartment_detail', pk=apartment.pk)

@login_required
def add_apartment(request):
    if request.method == 'POST':
        # بيانات مباشرة
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
        
        # حفظ الصور
        for image in request.FILES.getlist('images'):
            ApartmentImage.objects.create(apartment=apartment, image=image)
        
        messages.success(request, 'تم إضافة الشقة!')
        return redirect('my_apartments')
    
    return render(request, 'apartments/add_apartment_simple.html', {'universities': University.objects.all()})

# تم إزالة الاسم المستعار لأننا نستخدم دالة واحدة فقط

@login_required
def edit_apartment(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk)
    
    # التحقق من أن المستخدم هو مالك الشقة
    if apartment.owner != request.user:
        messages.error(request, 'ليس لديك صلاحية تعديل هذه الشقة.')
        return redirect('apartment_detail', pk=apartment.pk)
    
    if request.method == 'POST':
        form = ApartmentForm(request.POST, instance=apartment)
        if form.is_valid():
            form.save()
            
            images = request.FILES.getlist('image')
            if images:
                for image in images:
                    try:
                        ApartmentImage.objects.create(apartment=apartment, image=image)
                    except Exception as e:
                        print(f"Error saving image: {e}")
            
            messages.success(request, 'تم تحديث معلومات الشقة بنجاح!')
            return redirect('apartment_detail', pk=apartment.pk)
    else:
        form = ApartmentForm(instance=apartment)
        image_form = ApartmentImageForm()
    
    context = {
        'form': form,
        'image_form': image_form,
        'apartment': apartment,
        'settings': settings,
    }
    return render(request, 'apartments/edit_apartment.html', context)

@login_required
def delete_apartment(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk)
    
    # التحقق من أن المستخدم هو مالك الشقة
    if apartment.owner != request.user:
        messages.error(request, 'ليس لديك صلاحية حذف هذه الشقة.')
        return redirect('apartment_detail', pk=apartment.pk)
    
    if request.method == 'POST':
        apartment.delete()
        messages.success(request, 'تم حذف الشقة بنجاح!')
        return redirect('my_apartments')
    
    context = {
        'apartment': apartment,
    }
    return render(request, 'apartments/delete_apartment.html', context)

@login_required
def my_apartments(request):
    apartments = Apartment.objects.filter(owner=request.user)
    
    # تقسيم الشقق حسب الحالة
    pending_apartments = apartments.filter(status='pending')
    approved_apartments = apartments.filter(status='approved')
    rejected_apartments = apartments.filter(status='rejected')
    
    context = {
        'apartments': apartments,
        'pending_apartments': pending_apartments,
        'approved_apartments': approved_apartments,
        'rejected_apartments': rejected_apartments,
    }
    return render(request, 'apartments/my_apartments.html', context)

@login_required
def my_bookings(request):
    # الحصول على جميع حجوزات المستخدم
    bookings = Booking.objects.filter(student=request.user).order_by('-created_at')
    
    # تقسيم الحجوزات حسب الحالة
    pending_bookings = bookings.filter(status='pending')
    approved_bookings = bookings.filter(status='approved')
    rejected_bookings = bookings.filter(status='rejected')
    
    # الحجوزات النشطة (المعتمدة والتي لم تنتهي بعد)
    active_bookings = approved_bookings.filter(end_date__gte=timezone.now().date())
    
    # الحجوزات السابقة (المعتمدة والتي انتهت)
    past_bookings = approved_bookings.filter(end_date__lt=timezone.now().date())
    
    context = {
        'bookings': bookings,
        'pending_bookings': pending_bookings,
        'approved_bookings': approved_bookings,
        'rejected_bookings': rejected_bookings,
        'active_bookings': active_bookings,
        'past_bookings': past_bookings,
    }
    return render(request, 'apartments/my_bookings.html', context)

@login_required
def manage_bookings(request):
    # الحصول على جميع الحجوزات للشقق التي يملكها المستخدم
    bookings = Booking.objects.filter(apartment__owner=request.user)
    
    context = {
        'bookings': bookings,
    }
    return render(request, 'apartments/manage_bookings.html', context)

@login_required
def update_booking_status(request, pk, status):
    booking = get_object_or_404(Booking, pk=pk)
    
    # التحقق من أن المستخدم هو مالك الشقة
    if booking.apartment.owner != request.user:
        messages.error(request, 'ليس لديك صلاحية تحديث حالة هذا الحجز.')
        return redirect('manage_bookings')
    
    notification_type = ''
    notification_message = ''
    
    if status == 'approve':
        booking.status = 'approved'
        notification_type = 'booking_approved'
        notification_message = f'تمت الموافقة على طلب حجزك لشقة {booking.apartment.title}'
        messages.success(request, 'تمت الموافقة على الحجز بنجاح!')
    elif status == 'reject':
        booking.status = 'rejected'
        notification_type = 'booking_rejected'
        notification_message = f'تم رفض طلب حجزك لشقة {booking.apartment.title}'
        messages.success(request, 'تم رفض الحجز بنجاح!')
    elif status == 'non_serious':
        booking.status = 'non_serious'
        notification_type = 'non_serious_booking'
        
        # زيادة عداد عدم الجدية وتجميد الحساب عند تجاوز 3 مرات
        student_profile = booking.student.profile
        student_profile.non_serious_reports += 1
        
        if student_profile.non_serious_reports >= 3:
            student_profile.is_banned = True
            notification_message = f'تم الإبلاغ عنك كمستخدم غير جاد في حجز {booking.apartment.title}. تم تجميد حسابك بسبب تكرار عدم الجدية في الحجز. يرجى التواصل مع إدارة الموقع.'
            messages.success(request, 'تم الإبلاغ عن المستخدم كغير جاد في الحجز وتم تجميد حسابه بسبب تكرار عدم الجدية.')
            
            # إرسال إشعار للمسؤولين
            from django.contrib.auth.models import User
            admins = User.objects.filter(is_staff=True) | User.objects.filter(is_superuser=True)
            for admin in admins:
                Notification.objects.create(
                    user=admin,
                    notification_type='user_banned',
                    message=f'تم تجميد حساب {booking.student.username} بسبب تكرار عدم الجدية في الحجز.',
                )
        else:
            notification_message = f'تم الإبلاغ عنك كمستخدم غير جاد في حجز {booking.apartment.title}'
            messages.success(request, 'تم الإبلاغ عن المستخدم كغير جاد في الحجز.')
        
        student_profile.save()
        
        # إعادة الشقة للحالة المتاحة
        apartment = booking.apartment
        apartment.available = True
        apartment.save()
    
    booking.save()
    
    # إنشاء تنبيه للطالب فقط إذا تم تعيين نوع الإشعار
    if notification_type and notification_message:
        student_notification = Notification(
            user=booking.student,
            notification_type=notification_type,
            message=notification_message,
            related_booking=booking,
            related_apartment=booking.apartment
        )
        student_notification.save()
    
    return redirect('manage_bookings')

@login_required
def report_non_serious_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    
    # التحقق من أن المستخدم هو مالك الشقة
    if booking.apartment.owner != request.user:
        messages.error(request, 'ليس لديك صلاحية للإبلاغ عن هذا الحجز.')
        return redirect('owner_dashboard')
    
    booking.status = 'non_serious'
    booking.save()
    
    # زيادة عداد عدم الجدية
    student_profile = booking.student.profile
    student_profile.non_serious_reports += 1
    
    if student_profile.non_serious_reports >= 3:
        student_profile.is_banned = True
        messages.success(request, 'تم الإبلاغ عن المستخدم وتم تجميد حسابه')
    else:
        messages.success(request, 'تم الإبلاغ عن المستخدم بنجاح')
    
    student_profile.save()
    
    # إرسال إشعار للطالب
    Notification.objects.create(
        user=booking.student,
        notification_type='non_serious_booking',
        message=f'تم الإبلاغ عنك كمستخدم غير جاد في حجز {booking.apartment.title}',
        related_booking=booking,
        related_apartment=booking.apartment
    )
    
    return redirect('owner_dashboard')

@login_required
def toggle_wishlist(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk)
    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,
        apartment=apartment
    )
    
    if not created:
        # إذا كان موجودًا بالفعل، قم بإزالته
        wishlist_item.delete()
        is_in_wishlist = False
        message = 'تمت إزالة الشقة من المفضلات'
    else:
        is_in_wishlist = True
        message = 'تمت إضافة الشقة إلى المفضلات'
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'is_in_wishlist': is_in_wishlist,
            'message': message
        })
    
    messages.success(request, message)
    return redirect('apartment_detail', pk=apartment.pk)

@login_required
def my_wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('apartment')
    
    context = {
        'wishlist_items': wishlist_items,
    }
    return render(request, 'apartments/my_wishlist.html', context)


# تم إزالة دالة map_view لأننا لم نعد نستخدمها


@login_required
@user_passes_test(is_admin)
def admin_apartments(request):
    # الحصول على جميع الشقق مقسمة حسب الحالة
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
    notification = Notification(
        user=apartment.owner,
        notification_type='apartment_approved',
        message=f'تمت الموافقة على شقتك {apartment.title} وهي الآن معروضة للطلاب',
        related_apartment=apartment
    )
    notification.save()
    
    messages.success(request, 'تمت الموافقة على الشقة بنجاح!')
    return redirect('admin_apartments')

@login_required
@user_passes_test(is_admin)
def reject_apartment(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk)
    apartment.status = 'rejected'
    apartment.save()
    
    # إنشاء تنبيه للمالك
    notification = Notification(
        user=apartment.owner,
        notification_type='apartment_rejected',
        message=f'تم رفض شقتك {apartment.title}. يرجى مراجعة المعلومات والمحاولة مرة أخرى',
        related_apartment=apartment
    )
    notification.save()
    
    messages.success(request, 'تم رفض الشقة بنجاح!')
    return redirect('admin_apartments')

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    from django.contrib.auth.models import User
    
    # الإحصائيات العامة
    total_users = User.objects.count()
    total_apartments = Apartment.objects.count()
    pending_apartments = Apartment.objects.filter(status='pending').count()
    total_bookings = Booking.objects.count()
    
    # تفاصيل المستخدمين
    students_count = User.objects.filter(profile__user_type='student').count()
    owners_count = User.objects.filter(profile__user_type='owner').count()
    recent_students = User.objects.filter(profile__user_type='student').order_by('-date_joined')[:10]
    recent_owners = User.objects.filter(profile__user_type='owner').order_by('-date_joined')[:10]
    
    # الشقق
    approved_apartments = Apartment.objects.filter(status='approved').count()
    rejected_apartments = Apartment.objects.filter(status='rejected').count()
    pending_apartments_list = Apartment.objects.filter(status='pending').order_by('-created_at')[:10]
    
    # الحجوزات
    approved_bookings = Booking.objects.filter(status='approved').count()
    pending_bookings = Booking.objects.filter(status='pending').count()
    rejected_bookings = Booking.objects.filter(status='rejected').count()
    recent_bookings = Booking.objects.order_by('-created_at')[:10]
    
    context = {
        'total_users': total_users,
        'total_apartments': total_apartments,
        'pending_apartments': pending_apartments,
        'total_bookings': total_bookings,
        'students_count': students_count,
        'owners_count': owners_count,
        'recent_students': recent_students,
        'recent_owners': recent_owners,
        'approved_apartments': approved_apartments,
        'rejected_apartments': rejected_apartments,
        'pending_apartments_list': pending_apartments_list,
        'approved_bookings': approved_bookings,
        'pending_bookings': pending_bookings,
        'rejected_bookings': rejected_bookings,
        'recent_bookings': recent_bookings,
    }
    return render(request, 'apartments/admin_dashboard.html', context)

@login_required
def owner_dashboard(request):
    # إنشاء بروفايل إذا لم يكن موجود
    from users.models import Profile
    profile, created = Profile.objects.get_or_create(user=request.user)
    
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
    except Exception as e:
        # في حالة حدوث خطأ، عرض صفحة مبسطة
        return render(request, 'apartments/owner_dashboard_simple.html', {
            'user': request.user,
            'error': str(e)
        })