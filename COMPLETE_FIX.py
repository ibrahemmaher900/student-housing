#!/usr/bin/env python3
"""
إصلاح شامل لجميع مشاكل الموقع
"""

import os
import re

def fix_views():
    """إصلاح جميع الـ views"""
    
    # إصلاح approve_apartment
    approve_apartment_code = '''@login_required
@user_passes_test(is_admin)
def approve_apartment(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk)
    apartment.status = 'approved'
    apartment.save()
    
    # إنشاء تنبيه للمالك
    Notification.objects.create(
        user=apartment.owner,
        notification_type='apartment_approved',
        message=f'تمت الموافقة على شقتك {apartment.title} وهي الآن معروضة للطلاب',
        related_apartment=apartment
    )
    
    messages.success(request, 'تمت الموافقة على الشقة بنجاح!')
    return redirect('admin_apartments')'''
    
    # إصلاح reject_apartment
    reject_apartment_code = '''@login_required
@user_passes_test(is_admin)
def reject_apartment(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk)
    apartment.status = 'rejected'
    apartment.save()
    
    # إنشاء تنبيه للمالك
    Notification.objects.create(
        user=apartment.owner,
        notification_type='apartment_rejected',
        message=f'تم رفض شقتك {apartment.title}. يرجى مراجعة المعلومات والمحاولة مرة أخرى',
        related_apartment=apartment
    )
    
    messages.success(request, 'تم رفض الشقة بنجاح!')
    return redirect('admin_apartments')'''
    
    # إصلاح update_booking_status
    update_booking_code = '''@login_required
def update_booking_status(request, pk, status):
    booking = get_object_or_404(Booking, pk=pk)
    
    # التحقق من أن المستخدم هو مالك الشقة
    if booking.apartment.owner != request.user:
        messages.error(request, 'ليس لديك صلاحية تحديث حالة هذا الحجز.')
        return redirect('owner_dashboard')
    
    if status == 'approve':
        booking.status = 'approved'
        Notification.objects.create(
            user=booking.student,
            notification_type='booking_approved',
            message=f'تمت الموافقة على طلب حجزك لشقة {booking.apartment.title}',
            related_booking=booking,
            related_apartment=booking.apartment
        )
        messages.success(request, 'تمت الموافقة على الحجز بنجاح!')
    elif status == 'reject':
        booking.status = 'rejected'
        Notification.objects.create(
            user=booking.student,
            notification_type='booking_rejected',
            message=f'تم رفض طلب حجزك لشقة {booking.apartment.title}',
            related_booking=booking,
            related_apartment=booking.apartment
        )
        messages.success(request, 'تم رفض الحجز بنجاح!')
    
    booking.save()
    return redirect('owner_dashboard')'''
    
    # إصلاح report_non_serious_booking
    report_code = '''@login_required
def report_non_serious_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    
    # التحقق من أن المستخدم هو مالك الشقة
    if booking.apartment.owner != request.user:
        messages.error(request, 'ليس لديك صلاحية لهذا الإجراء.')
        return redirect('owner_dashboard')
    
    booking.status = 'non_serious'
    booking.save()
    
    # زيادة عداد عدم الجدية
    student_profile = booking.student.profile
    student_profile.non_serious_reports += 1
    
    if student_profile.non_serious_reports >= 3:
        student_profile.is_banned = True
        message = f'تم الإبلاغ عنك كمستخدم غير جاد في حجز {booking.apartment.title}. تم تجميد حسابك بسبب تكرار عدم الجدية.'
    else:
        message = f'تم الإبلاغ عنك كمستخدم غير جاد في حجز {booking.apartment.title}'
    
    student_profile.save()
    
    # إنشاء تنبيه للطالب
    Notification.objects.create(
        user=booking.student,
        notification_type='non_serious_booking',
        message=message,
        related_booking=booking,
        related_apartment=booking.apartment
    )
    
    # إعادة الشقة للحالة المتاحة
    apartment = booking.apartment
    apartment.available = True
    apartment.save()
    
    messages.success(request, 'تم الإبلاغ عن المستخدم بنجاح.')
    return redirect('owner_dashboard')'''
    
    print("✅ تم إنشاء كود الـ views المحدث")
    return {
        'approve_apartment': approve_apartment_code,
        'reject_apartment': reject_apartment_code,
        'update_booking_status': update_booking_code,
        'report_non_serious_booking': report_code
    }

def fix_templates():
    """إصلاح جميع الـ templates"""
    
    # admin_apartments.html - أزرار الموافقة والرفض
    admin_buttons = '''<div class="d-flex">
    <a href="{% url 'apartment_detail' apartment.id %}" class="btn btn-sm btn-outline-primary me-2">
        <i class="fas fa-eye me-1"></i> عرض
    </a>
    <form method="post" action="{% url 'approve_apartment' apartment.id %}" style="display: inline;" onsubmit="return confirm('هل أنت متأكد من اعتماد هذه الشقة؟')">
        {% csrf_token %}
        <button type="submit" class="btn btn-sm btn-success me-2">
            <i class="fas fa-check me-1"></i> موافقة
        </button>
    </form>
    <form method="post" action="{% url 'reject_apartment' apartment.id %}" style="display: inline;" onsubmit="return confirm('هل أنت متأكد من رفض هذه الشقة؟')">
        {% csrf_token %}
        <button type="submit" class="btn btn-sm btn-danger">
            <i class="fas fa-times me-1"></i> رفض
        </button>
    </form>
</div>'''
    
    # owner_dashboard.html - أزرار الحجوزات
    owner_buttons = '''{% if booking.status == 'pending' %}
<div class="btn-group" role="group">
    <form method="post" action="{% url 'update_booking_status' booking.id 'approve' %}" style="display: inline;" onsubmit="return confirm('هل أنت متأكد من قبول هذا الحجز؟')">
        {% csrf_token %}
        <button type="submit" class="btn btn-sm btn-success">قبول</button>
    </form>
    <form method="post" action="{% url 'update_booking_status' booking.id 'reject' %}" style="display: inline;" onsubmit="return confirm('هل أنت متأكد من رفض هذا الحجز؟')">
        {% csrf_token %}
        <button type="submit" class="btn btn-sm btn-danger">رفض</button>
    </form>
</div>
{% elif booking.status == 'approved' %}
<form method="post" action="{% url 'report_non_serious_booking' booking.id %}" style="display: inline;" onsubmit="return confirm('هل أنت متأكد من الإبلاغ عن هذا المستخدم؟')">
    {% csrf_token %}
    <button type="submit" class="btn btn-sm btn-warning">إبلاغ عن عدم الجدية</button>
</form>
{% endif %}'''
    
    print("✅ تم إنشاء كود الـ templates المحدث")
    return {
        'admin_buttons': admin_buttons,
        'owner_buttons': owner_buttons
    }

def create_simple_views_file():
    """إنشاء ملف views مبسط وعملي"""
    
    simple_views = '''from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from .models import Apartment, Booking, Notification
from users.models import Profile

def is_admin(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_admin)
def approve_apartment(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk)
    apartment.status = 'approved'
    apartment.save()
    
    Notification.objects.create(
        user=apartment.owner,
        notification_type='apartment_approved',
        message=f'تمت الموافقة على شقتك {apartment.title}',
        related_apartment=apartment
    )
    
    messages.success(request, 'تمت الموافقة على الشقة!')
    return redirect('admin_apartments')

@login_required
@user_passes_test(is_admin)
def reject_apartment(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk)
    apartment.status = 'rejected'
    apartment.save()
    
    Notification.objects.create(
        user=apartment.owner,
        notification_type='apartment_rejected',
        message=f'تم رفض شقتك {apartment.title}',
        related_apartment=apartment
    )
    
    messages.success(request, 'تم رفض الشقة!')
    return redirect('admin_apartments')

@login_required
def update_booking_status(request, pk, status):
    booking = get_object_or_404(Booking, pk=pk)
    
    if booking.apartment.owner != request.user:
        messages.error(request, 'ليس لديك صلاحية!')
        return redirect('owner_dashboard')
    
    if status == 'approve':
        booking.status = 'approved'
        msg = 'تمت الموافقة على الحجز!'
    elif status == 'reject':
        booking.status = 'rejected'
        msg = 'تم رفض الحجز!'
    
    booking.save()
    messages.success(request, msg)
    return redirect('owner_dashboard')

@login_required
def report_non_serious_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    
    if booking.apartment.owner != request.user:
        messages.error(request, 'ليس لديك صلاحية!')
        return redirect('owner_dashboard')
    
    booking.status = 'non_serious'
    booking.save()
    
    profile = booking.student.profile
    profile.non_serious_reports += 1
    if profile.non_serious_reports >= 3:
        profile.is_banned = True
    profile.save()
    
    messages.success(request, 'تم الإبلاغ!')
    return redirect('owner_dashboard')
'''
    
    with open('/Users/ibrahemmaher/student_housing/apartments/views_simple_fix.py', 'w') as f:
        f.write(simple_views)
    
    print("✅ تم إنشاء ملف views_simple_fix.py")

def main():
    print("🔧 بدء الإصلاح الشامل للموقع...")
    print()
    
    # إصلاح الـ views
    views_code = fix_views()
    
    # إصلاح الـ templates
    templates_code = fix_templates()
    
    # إنشاء ملف views مبسط
    create_simple_views_file()
    
    print()
    print("📋 الخطوات المطلوبة:")
    print("1. استبدال الـ views في apartments/views.py")
    print("2. تحديث الـ templates")
    print("3. التأكد من وجود CSRF tokens")
    print("4. اختبار الأزرار")
    print()
    print("🎯 الحل النهائي:")
    print("- استخدام forms مع POST method")
    print("- إضافة CSRF protection")
    print("- رسائل تأكيد JavaScript")
    print("- معالجة الأخطاء")
    print()
    print("✅ تم إنشاء جميع الملفات المطلوبة!")

if __name__ == "__main__":
    main()