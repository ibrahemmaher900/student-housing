# إصلاح مشكلة لوحات التحكم على Render

## المشكلة
```
AttributeError: module 'apartments.views' has no attribute 'owner_dashboard'
```

## الحل السريع

### الطريقة الأولى: استخدام Git
```bash
git add .
git commit -m "إضافة دوال لوحات التحكم المفقودة"
git push origin main
```

### الطريقة الثانية: إصلاح مباشر على الخادم
1. اتصل بالخادم عبر SSH أو استخدم console
2. انتقل إلى مجلد المشروع:
```bash
cd /opt/render/project/src
```

3. شغل ملف الإصلاح:
```bash
bash fix_dashboard.sh
```

### الطريقة الثالثة: إضافة يدوية
أضف الكود التالي لنهاية ملف `apartments/views.py`:

```python
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """لوحة تحكم المسؤول"""
    from django.contrib.auth.models import User
    
    total_users = User.objects.count()
    total_apartments = Apartment.objects.count()
    pending_apartments = Apartment.objects.filter(status='pending').count()
    approved_apartments = Apartment.objects.filter(status='approved').count()
    rejected_apartments = Apartment.objects.filter(status='rejected').count()
    total_bookings = Booking.objects.count()
    pending_bookings = Booking.objects.filter(status='pending').count()
    approved_bookings = Booking.objects.filter(status='approved').count()
    rejected_bookings = Booking.objects.filter(status='rejected').count()
    
    students_count = User.objects.filter(profile__user_type='student').count()
    owners_count = User.objects.filter(profile__user_type='owner').count()
    
    recent_students = User.objects.filter(profile__user_type='student').order_by('-date_joined')[:10]
    recent_owners = User.objects.filter(profile__user_type='owner').order_by('-date_joined')[:10]
    
    pending_apartments_list = Apartment.objects.filter(status='pending').order_by('-created_at')[:10]
    recent_bookings = Booking.objects.order_by('-created_at')[:10]
    
    context = {
        'total_users': total_users,
        'total_apartments': total_apartments,
        'pending_apartments': pending_apartments,
        'approved_apartments': approved_apartments,
        'rejected_apartments': rejected_apartments,
        'total_bookings': total_bookings,
        'pending_bookings': pending_bookings,
        'approved_bookings': approved_bookings,
        'rejected_bookings': rejected_bookings,
        'students_count': students_count,
        'owners_count': owners_count,
        'recent_students': recent_students,
        'recent_owners': recent_owners,
        'pending_apartments_list': pending_apartments_list,
        'recent_bookings': recent_bookings,
    }
    return render(request, 'apartments/admin_dashboard.html', context)

@login_required
def owner_dashboard(request):
    """لوحة تحكم مالك العقار"""
    apartments = Apartment.objects.filter(owner=request.user)
    total_apartments = apartments.count()
    approved_apartments = apartments.filter(status='approved').count()
    pending_apartments = apartments.filter(status='pending').count()
    rejected_apartments = apartments.filter(status='rejected').count()
    
    bookings = Booking.objects.filter(apartment__owner=request.user).order_by('-created_at')
    total_bookings = bookings.count()
    pending_bookings = bookings.filter(status='pending').count()
    approved_bookings = bookings.filter(status='approved').count()
    rejected_bookings = bookings.filter(status='rejected').count()
    
    context = {
        'apartments': apartments,
        'total_apartments': total_apartments,
        'approved_apartments': approved_apartments,
        'pending_apartments': pending_apartments,
        'rejected_apartments': rejected_apartments,
        'bookings': bookings,
        'total_bookings': total_bookings,
        'pending_bookings': pending_bookings,
        'approved_bookings': approved_bookings,
        'rejected_bookings': rejected_bookings,
    }
    return render(request, 'apartments/owner_dashboard.html', context)
```

## بعد الإصلاح
أعد تشغيل الخادم وستعمل لوحات التحكم بشكل طبيعي:
- `/apartments/admin/dashboard/` - لوحة تحكم الأدمن
- `/apartments/owner/dashboard/` - لوحة تحكم مالك العقار