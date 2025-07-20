#!/usr/bin/env python
"""
سكريبت لتهيئة قاعدة البيانات وإنشاء الجداول
"""
import os
import sys
import django

# إعداد Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_housing.settings')
django.setup()

from django.core.management import call_command
from django.db import connection

def initialize_database():
    """تهيئة قاعدة البيانات وإنشاء الجداول"""
    print("جاري تهيئة قاعدة البيانات...")
    
    # طباعة الجداول الموجودة
    tables = connection.introspection.table_names()
    print(f"الجداول الموجودة قبل الترحيل: {tables}")
    
    # إنشاء ملفات الترحيل
    print("جاري إنشاء ملفات الترحيل...")
    call_command('makemigrations')
    
    # تطبيق الترحيلات
    print("جاري تطبيق الترحيلات...")
    call_command('migrate')
    
    # التحقق من الجداول بعد الترحيل
    tables = connection.introspection.table_names()
    print(f"الجداول الموجودة بعد الترحيل: {tables}")
    
    # التحقق من وجود جدول apartments_apartment
    if 'apartments_apartment' in tables:
        print("تم إنشاء جدول apartments_apartment بنجاح")
    else:
        print("فشل في إنشاء جدول apartments_apartment!")
        
    print("اكتملت تهيئة قاعدة البيانات")

if __name__ == "__main__":
    initialize_database()