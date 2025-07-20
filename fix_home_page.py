#!/usr/bin/env python
"""
سكريبت لإصلاح مشكلة الصفحة الرئيسية
"""
import os
import sys
import django

# إعداد Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_housing.settings')
django.setup()

from django.db import connection
from django.core.management import call_command

def fix_home_page():
    """إصلاح مشكلة الصفحة الرئيسية"""
    print("جاري إصلاح مشكلة الصفحة الرئيسية...")
    
    # التحقق من وجود جداول قاعدة البيانات
    tables = connection.introspection.table_names()
    print(f"الجداول الموجودة: {tables}")
    
    # إنشاء جدول apartments_apartment إذا لم يكن موجودًا
    if 'apartments_apartment' not in tables:
        print("جدول apartments_apartment غير موجود، جاري إنشاؤه...")
        
        # تطبيق الترحيلات
        call_command('migrate', 'apartments', interactive=False)
        
        # التحقق مرة أخرى
        tables = connection.introspection.table_names()
        if 'apartments_apartment' in tables:
            print("تم إنشاء جدول apartments_apartment بنجاح")
        else:
            print("فشل في إنشاء جدول apartments_apartment")
            
            # محاولة إنشاء الجدول يدويًا
            with connection.cursor() as cursor:
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS apartments_apartment (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    description TEXT,
                    price DECIMAL(10, 2) NOT NULL,
                    deposit DECIMAL(10, 2) DEFAULT 0,
                    city VARCHAR(100) NOT NULL,
                    district VARCHAR(100) NOT NULL,
                    address TEXT NOT NULL,
                    latitude DECIMAL(9, 6),
                    longitude DECIMAL(9, 6),
                    rooms INTEGER NOT NULL,
                    area DECIMAL(8, 2) NOT NULL,
                    floor INTEGER NOT NULL,
                    furnished BOOLEAN NOT NULL,
                    gender VARCHAR(10) NOT NULL,
                    payment_method VARCHAR(20) NOT NULL,
                    bills_included BOOLEAN NOT NULL,
                    available BOOLEAN NOT NULL DEFAULT TRUE,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    owner_id INTEGER NOT NULL,
                    university_id INTEGER,
                    distance_to_university DECIMAL(5, 2),
                    walking_time INTEGER,
                    driving_time INTEGER,
                    google_maps_link VARCHAR(255),
                    contact_name VARCHAR(100) NOT NULL,
                    phone VARCHAR(20) NOT NULL,
                    whatsapp_available BOOLEAN NOT NULL,
                    additional_contact TEXT,
                    advertiser_type VARCHAR(20) NOT NULL,
                    conditions TEXT,
                    additional_description TEXT,
                    has_wifi BOOLEAN NOT NULL DEFAULT FALSE,
                    has_ac BOOLEAN NOT NULL DEFAULT FALSE,
                    has_fridge BOOLEAN NOT NULL DEFAULT FALSE,
                    has_washer BOOLEAN NOT NULL DEFAULT FALSE,
                    has_kitchen BOOLEAN NOT NULL DEFAULT FALSE,
                    has_private_bathroom BOOLEAN NOT NULL DEFAULT FALSE,
                    has_balcony BOOLEAN NOT NULL DEFAULT FALSE,
                    has_parking BOOLEAN NOT NULL DEFAULT FALSE,
                    apartment_type VARCHAR(20) NOT NULL DEFAULT 'apartment'
                );
                """)
                print("تم إنشاء جدول apartments_apartment يدويًا")
    else:
        print("جدول apartments_apartment موجود بالفعل")
    
    # إنشاء جدول apartments_university إذا لم يكن موجودًا
    if 'apartments_university' not in tables:
        print("جدول apartments_university غير موجود، جاري إنشاؤه...")
        
        # تطبيق الترحيلات
        call_command('migrate', 'apartments', interactive=False)
        
        # التحقق مرة أخرى
        tables = connection.introspection.table_names()
        if 'apartments_university' in tables:
            print("تم إنشاء جدول apartments_university بنجاح")
        else:
            print("فشل في إنشاء جدول apartments_university")
            
            # محاولة إنشاء الجدول يدويًا
            with connection.cursor() as cursor:
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS apartments_university (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    city VARCHAR(100) NOT NULL,
                    address TEXT,
                    latitude DECIMAL(9, 6),
                    longitude DECIMAL(9, 6),
                    website VARCHAR(255),
                    logo VARCHAR(255)
                );
                """)
                print("تم إنشاء جدول apartments_university يدويًا")
                
                # إدخال بيانات افتراضية للجامعات
                cursor.execute("""
                INSERT INTO apartments_university (name, city)
                VALUES ('جامعة القاهرة', 'القاهرة'),
                       ('جامعة عين شمس', 'القاهرة'),
                       ('جامعة الإسكندرية', 'الإسكندرية');
                """)
                print("تم إدخال بيانات افتراضية للجامعات")
    else:
        print("جدول apartments_university موجود بالفعل")
    
    # إنشاء مستخدم مسؤول إذا لم يكن موجودًا
    from django.contrib.auth.models import User
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("تم إنشاء مستخدم مسؤول: admin / admin123")
    else:
        print("مستخدم مسؤول موجود بالفعل")
    
    print("اكتملت عملية إصلاح الصفحة الرئيسية")

if __name__ == "__main__":
    fix_home_page()