#!/usr/bin/env python3
"""
اختبار إصلاح AJAX للأزرار
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

def test_ajax_booking():
    print("🧪 اختبار AJAX للحجوزات...")
    
    try:
        # إنشاء بيانات الاختبار
        owner = User.objects.create_user('owner_test', 'owner@test.com', 'pass123')
        student = User.objects.create_user('student_test', 'student@test.com', 'pass123')
        
        Profile.objects.create(user=owner, user_type='owner')
        Profile.objects.create(user=student, user_type='student')
        
        university = University.objects.create(name='جامعة الاختبار', city='القاهرة')
        
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
        
        booking = Booking.objects.create(
            apartment=apartment,
            student=student,
            start_date='2024-01-01',
            end_date='2024-12-31',
            status='pending'
        )
        
        # اختبار AJAX request
        client = Client()
        client.login(username='owner_test', password='pass123')
        
        response = client.post(
            f'/apartments/booking/{booking.id}/approve/',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.content.decode()}")
        
        if response.status_code == 200:
            import json
            data = json.loads(response.content)
            if data.get('success'):
                print("✅ AJAX يعمل بشكل صحيح")
                
                # التحقق من تحديث قاعدة البيانات
                booking.refresh_from_db()
                if booking.status == 'approved':
                    print("✅ تم تحديث قاعدة البيانات")
                else:
                    print(f"❌ لم يتم تحديث قاعدة البيانات: {booking.status}")
            else:
                print("❌ AJAX لا يعمل بشكل صحيح")
        else:
            print(f"❌ خطأ في الاستجابة: {response.status_code}")
        
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
    test_ajax_booking()