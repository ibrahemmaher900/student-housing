#!/usr/bin/env python3
"""
اختبار رفع الملفات
"""

import os
import sys
import django
from django.core.files.uploadedfile import SimpleUploadedFile

# إعداد Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_housing.settings')
django.setup()

from django.contrib.auth.models import User
from apartments.models import Apartment, ApartmentImage, University

def test_apartment_creation():
    """اختبار إنشاء شقة"""
    print("🧪 اختبار إنشاء شقة...")
    
    try:
        # إنشاء مستخدم تجريبي
        user, created = User.objects.get_or_create(
            username='test_user',
            defaults={'email': 'test@example.com'}
        )
        
        # إنشاء جامعة تجريبية
        university, created = University.objects.get_or_create(
            name='جامعة تجريبية',
            defaults={'city': 'القاهرة'}
        )
        
        # إنشاء شقة
        apartment = Apartment.objects.create(
            title='شقة تجريبية',
            description='وصف تجريبي',
            price=1000,
            apartment_type='studio',
            area=50,
            bedrooms=1,
            bathrooms=1,
            address='عنوان تجريبي',
            distance_to_university=1.0,
            university=university,
            owner=user,
            status='pending'
        )
        
        print(f"✅ تم إنشاء الشقة بنجاح: {apartment.id}")
        
        # حذف الشقة التجريبية
        apartment.delete()
        print("✅ تم حذف الشقة التجريبية")
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في إنشاء الشقة: {e}")
        return False

def test_image_upload():
    """اختبار رفع الصور"""
    print("\n📸 اختبار رفع الصور...")
    
    try:
        # إنشاء ملف صورة تجريبي
        image_content = b'fake image content'
        image_file = SimpleUploadedFile(
            "test.jpg",
            image_content,
            content_type="image/jpeg"
        )
        
        # إنشاء مستخدم وجامعة
        user, _ = User.objects.get_or_create(
            username='test_user2',
            defaults={'email': 'test2@example.com'}
        )
        
        university, _ = University.objects.get_or_create(
            name='جامعة تجريبية 2',
            defaults={'city': 'الإسكندرية'}
        )
        
        # إنشاء شقة
        apartment = Apartment.objects.create(
            title='شقة للاختبار',
            description='اختبار الصور',
            price=1500,
            apartment_type='studio',
            area=60,
            bedrooms=1,
            bathrooms=1,
            address='عنوان للاختبار',
            distance_to_university=2.0,
            university=university,
            owner=user,
            status='pending'
        )
        
        # رفع صورة
        apartment_image = ApartmentImage.objects.create(
            apartment=apartment,
            image=image_file\n        )\n        \n        print(f\"✅ تم رفع الصورة بنجاح: {apartment_image.id}\")\n        \n        # حذف الاختبار\n        apartment.delete()\n        print(\"✅ تم حذف بيانات الاختبار\")\n        \n        return True\n        \n    except Exception as e:\n        print(f\"❌ خطأ في رفع الصورة: {e}\")\n        return False\n\ndef main():\n    \"\"\"الدالة الرئيسية\"\"\"\n    print(\"🚀 بدء اختبار رفع الملفات...\")\n    print(\"=\" * 50)\n    \n    # تشغيل الاختبارات\n    test1 = test_apartment_creation()\n    test2 = test_image_upload()\n    \n    print(\"\\n\" + \"=\" * 50)\n    if test1 and test2:\n        print(\"✅ جميع الاختبارات نجحت!\")\n        print(\"🎉 رفع الملفات يعمل بشكل صحيح!\")\n    else:\n        print(\"❌ بعض الاختبارات فشلت\")\n        print(\"🔧 يحتاج إلى إصلاح\")\n\nif __name__ == '__main__':\n    main()