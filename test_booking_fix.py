#!/usr/bin/env python3
"""
اختبار إصلاح زر الموافقة على الحجز
"""

import os
import django
import sys

# إعداد Django
sys.path.append('/Users/ibrahemmaher/student_housing')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_housing.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from apartments.models import Apartment, Booking, University
from users.models import Profile

def test_booking_approval():
    print("🧪 اختبار زر الموافقة على الحجز...")
    
    try:
        # إنشاء مستخدمين للاختبار
        owner = User.objects.create_user('test_owner', 'owner@test.com', 'pass123')
        student = User.objects.create_user('test_student', 'student@test.com', 'pass123')
        
        # إنشاء profiles
        Profile.objects.create(user=owner, user_type='owner')
        Profile.objects.create(user=student, user_type='student')
        
        # إنشاء جامعة
        university = University.objects.create(name='جامعة الاختبار', city='القاهرة')
        
        # إنشاء شقة
        apartment = Apartment.objects.create(
            title='شقة اختبار',
            description='شقة للاختبار',
            price=1000,
            apartment_type='studio',
            area=50,
            bedrooms=1,
            bathrooms=1,
            address='عنوان اختبار',
            distance_to_university=1.0,
            university=university,
            owner=owner,
            status='approved'
        )
        
        # إنشاء حجز
        booking = Booking.objects.create(
            apartment=apartment,
            student=student,
            start_date='2024-01-01',
            end_date='2024-12-31',
            status='pending'
        )
        
        print(f"✅ تم إنشاء حجز رقم {booking.id}")
        
        # اختبار الموافقة
        client = Client()
        client.login(username='test_owner', password='pass123')
        
        response = client.post(f'/apartments/booking/{booking.id}/approve/', 
                             HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        if response.status_code == 200:
            print("✅ تم إرسال طلب الموافقة بنجاح")
            
            # التحقق من تحديث الحالة
            booking.refresh_from_db()
            if booking.status == 'approved':
                print("✅ تم تحديث حالة الحجز إلى 'approved'")
            else:
                print(f"❌ حالة الحجز لم تتغير: {booking.status}")
        else:
            print(f"❌ فشل في إرسال الطلب: {response.status_code}")
            print(response.content.decode())
        
        # تنظيف البيانات
        booking.delete()
        apartment.delete()
        university.delete()
        owner.delete()
        student.delete()
        
        print("🎉 انتهى الاختبار")
        
    except Exception as e:
        print(f"❌ خطأ في الاختبار: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_booking_approval()