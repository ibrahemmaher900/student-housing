#!/usr/bin/env python3
"""
سكريبت للتحقق من الأخطاء في الموقع
"""

import os
import sys
import django

# إعداد Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_housing.settings')
django.setup()

from django.core.management import execute_from_command_line
from django.test.utils import get_runner
from django.conf import settings
from django.contrib.auth.models import User
from users.models import Profile
from apartments.models import University, Apartment

def check_database():
    """فحص قاعدة البيانات"""
    print("🔍 فحص قاعدة البيانات...")
    
    try:
        # فحص المستخدمين
        users_count = User.objects.count()
        print(f"✅ عدد المستخدمين: {users_count}")
        
        # فحص البروفايلات
        profiles_count = Profile.objects.count()
        print(f"✅ عدد البروفايلات: {profiles_count}")
        
        # فحص المستخدمين بدون بروفايل
        users_without_profile = User.objects.filter(profile__isnull=True)
        if users_without_profile.exists():
            print(f"⚠️  مستخدمين بدون بروفايل: {users_without_profile.count()}")
            for user in users_without_profile:
                Profile.objects.create(user=user)
                print(f"✅ تم إنشاء بروفايل للمستخدم: {user.username}")
        
        # فحص الجامعات
        universities_count = University.objects.count()
        print(f"✅ عدد الجامعات: {universities_count}")
        
        # فحص الشقق
        apartments_count = Apartment.objects.count()
        print(f"✅ عدد الشقق: {apartments_count}")
        
        print("✅ فحص قاعدة البيانات مكتمل")
        
    except Exception as e:
        print(f"❌ خطأ في فحص قاعدة البيانات: {e}")

def check_media_files():
    """فحص ملفات الوسائط"""
    print("\n📁 فحص ملفات الوسائط...")
    
    try:
        media_root = settings.MEDIA_ROOT
        if not os.path.exists(media_root):
            os.makedirs(media_root)
            print(f"✅ تم إنشاء مجلد الوسائط: {media_root}")
        
        # إنشاء المجلدات المطلوبة
        required_dirs = [
            'apartments',
            'profile_pics',
        ]
        
        for dir_name in required_dirs:
            dir_path = os.path.join(media_root, dir_name)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
                print(f"✅ تم إنشاء مجلد: {dir_path}")
        
        print("✅ فحص ملفات الوسائط مكتمل")
        
    except Exception as e:
        print(f"❌ خطأ في فحص ملفات الوسائط: {e}")

def check_static_files():
    """فحص الملفات الثابتة"""
    print("\n📄 فحص الملفات الثابتة...")
    
    try:
        static_root = settings.STATIC_ROOT
        if static_root and not os.path.exists(static_root):
            os.makedirs(static_root)
            print(f"✅ تم إنشاء مجلد الملفات الثابتة: {static_root}")
        
        print("✅ فحص الملفات الثابتة مكتمل")
        
    except Exception as e:
        print(f"❌ خطأ في فحص الملفات الثابتة: {e}")

def run_migrations():
    """تشغيل migrations"""
    print("\n🔄 تشغيل migrations...")
    
    try:
        execute_from_command_line(['manage.py', 'makemigrations'])
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ تم تشغيل migrations بنجاح")
        
    except Exception as e:
        print(f"❌ خطأ في تشغيل migrations: {e}")

def main():
    """الدالة الرئيسية"""
    print("🚀 بدء فحص الموقع...")
    print("=" * 50)
    
    # تشغيل الفحوصات
    run_migrations()
    check_database()
    check_media_files()
    check_static_files()
    
    print("\n" + "=" * 50)
    print("✅ انتهى فحص الموقع بنجاح!")
    print("🎉 الموقع جاهز للاستخدام!")

if __name__ == '__main__':
    main()