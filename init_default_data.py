#!/usr/bin/env python
"""
سكريبت لتهيئة بيانات افتراضية للتطبيق
"""
import os
import sys
import django

# إعداد Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_housing.settings')
django.setup()

from django.contrib.auth.models import User
from django.db import transaction
from apartments.models import University

def create_default_data():
    """إنشاء بيانات افتراضية للتطبيق"""
    print("جاري إنشاء بيانات افتراضية...")
    
    # إنشاء مستخدم مسؤول
    try:
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            print("تم إنشاء مستخدم مسؤول: admin / admin123")
    except Exception as e:
        print(f"خطأ في إنشاء مستخدم مسؤول: {e}")
    
    # إنشاء جامعات افتراضية
    try:
        with transaction.atomic():
            if University.objects.count() == 0:
                universities = [
                    {'name': 'جامعة القاهرة', 'city': 'القاهرة'},
                    {'name': 'جامعة عين شمس', 'city': 'القاهرة'},
                    {'name': 'جامعة الإسكندرية', 'city': 'الإسكندرية'},
                ]
                
                for uni_data in universities:
                    University.objects.create(**uni_data)
                
                print(f"تم إنشاء {len(universities)} جامعات افتراضية")
    except Exception as e:
        print(f"خطأ في إنشاء الجامعات: {e}")
    
    print("اكتملت تهيئة البيانات الافتراضية")

if __name__ == "__main__":
    create_default_data()