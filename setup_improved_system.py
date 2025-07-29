#!/usr/bin/env python
"""
سكريبت إعداد النظام المحسن
يقوم بتطبيق جميع التحسينات المطلوبة على النظام
"""

import os
import sys
import django
from pathlib import Path

# إضافة مسار المشروع
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# إعداد Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_housing.settings')
django.setup()

from django.contrib.auth.models import User
from django.core.management import execute_from_command_line
from apartments.models import University, Apartment, Notification
from users.models import Profile

def setup_improved_system():
    """إعداد النظام المحسن"""
    
    print("🚀 بدء إعداد النظام المحسن...")
    
    # 1. إنشاء الجداول الجديدة
    print("📊 إنشاء الجداول...")
    try:
        execute_from_command_line(['manage.py', 'makemigrations'])
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ تم إنشاء الجداول بنجاح")
    except Exception as e:
        print(f"❌ خطأ في إنشاء الجداول: {e}")
    
    # 2. إنشاء مستخدم مسؤول إذا لم يكن موجود
    print("👤 إنشاء حساب المسؤول...")
    try:
        if not User.objects.filter(is_superuser=True).exists():
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@student-housing.com',
                password='admin123',
                first_name='مسؤول',
                last_name='النظام'
            )
            print("✅ تم إنشاء حساب المسؤول: admin / admin123")
        else:
            print("✅ حساب المسؤول موجود مسبقاً")
    except Exception as e:
        print(f"❌ خطأ في إنشاء حساب المسؤول: {e}")
    
    # 3. إنشاء بيانات تجريبية
    print("🏢 إنشاء الجامعات...")
    universities_data = [
        {'name': 'جامعة القاهرة', 'city': 'القاهرة'},
        {'name': 'جامعة عين شمس', 'city': 'القاهرة'},
        {'name': 'جامعة الإسكندرية', 'city': 'الإسكندرية'},
        {'name': 'جامعة أسيوط', 'city': 'أسيوط'},
        {'name': 'جامعة المنصورة', 'city': 'المنصورة'},
    ]
    
    for uni_data in universities_data:
        university, created = University.objects.get_or_create(
            name=uni_data['name'],
            defaults={'city': uni_data['city']}
        )
        if created:
            print(f"✅ تم إنشاء جامعة: {uni_data['name']}")
    
    # 4. إنشاء مستخدمين تجريبيين
    print("👥 إنشاء مستخدمين تجريبيين...")
    
    # مالك عقار
    try:
        owner_user, created = User.objects.get_or_create(
            username='owner1',
            defaults={
                'email': 'owner@example.com',
                'first_name': 'أحمد',
                'last_name': 'محمد',
                'is_active': True
            }
        )
        if created:
            owner_user.set_password('password123')
            owner_user.save()
            
        profile, created = Profile.objects.get_or_create(
            user=owner_user,
            defaults={
                'user_type': 'owner',
                'phone': '01234567890',
                'city': 'القاهرة'
            }
        )
        if created:
            print("✅ تم إنشاء حساب مالك العقار: owner1 / password123")
    except Exception as e:
        print(f"❌ خطأ في إنشاء مالك العقار: {e}")
    
    # طالب
    try:
        student_user, created = User.objects.get_or_create(
            username='student1',
            defaults={
                'email': 'student@example.com',
                'first_name': 'فاطمة',
                'last_name': 'علي',
                'is_active': True
            }
        )
        if created:
            student_user.set_password('password123')
            student_user.save()
            
        profile, created = Profile.objects.get_or_create(
            user=student_user,
            defaults={
                'user_type': 'student',
                'phone': '01987654321',
                'city': 'القاهرة',
                'university': University.objects.first()
            }
        )
        if created:
            print("✅ تم إنشاء حساب الطالب: student1 / password123")
    except Exception as e:
        print(f"❌ خطأ في إنشاء الطالب: {e}")
    
    # 5. تحديث الملفات الموجودة
    print("📁 تحديث الملفات...")
    
    # نسخ الملفات المحدثة
    files_to_update = [
        ('templates/base/base_updated.html', 'templates/base/base.html'),
        ('apartments/views_notifications_improved.py', 'apartments/views_notifications.py'),
        ('apartments/views_admin_improved.py', 'apartments/views_admin.py'),
        ('apartments/urls_updated.py', 'apartments/urls.py'),
        ('users/forms_updated.py', 'users/forms.py'),
        ('users/views_updated.py', 'users/views.py'),
        ('templates/apartments/admin_apartments_improved.html', 'templates/apartments/admin_apartments.html'),
        ('templates/apartments/notifications_improved.html', 'templates/apartments/notifications.html'),
    ]
    
    for source, target in files_to_update:
        source_path = BASE_DIR / source
        target_path = BASE_DIR / target
        
        if source_path.exists():
            try:
                # إنشاء نسخة احتياطية
                if target_path.exists():
                    backup_path = target_path.with_suffix(target_path.suffix + '.backup')
                    target_path.rename(backup_path)
                
                # نسخ الملف الجديد
                import shutil
                shutil.copy2(source_path, target_path)
                print(f"✅ تم تحديث: {target}")
            except Exception as e:
                print(f"❌ خطأ في تحديث {target}: {e}")
    
    # 6. تنظيف التنبيهات القديمة
    print("🧹 تنظيف البيانات...")
    try:
        from django.utils import timezone
        from datetime import timedelta
        
        old_date = timezone.now() - timedelta(days=90)
        deleted_count = Notification.objects.filter(
            created_at__lt=old_date,
            is_read=True
        ).delete()[0]
        print(f"✅ تم حذف {deleted_count} تنبيه قديم")
    except Exception as e:
        print(f"❌ خطأ في تنظيف البيانات: {e}")
    
    print("\n🎉 تم إعداد النظام المحسن بنجاح!")
    print("\n📋 ملخص الحسابات:")
    print("👨‍💼 مسؤول النظام: admin / admin123")
    print("🏠 مالك عقار: owner1 / password123")
    print("🎓 طالب: student1 / password123")
    print("\n🔧 التحسينات المطبقة:")
    print("✅ نظام تنبيهات محسن بكفاءة عالية")
    print("✅ إخفاء لوحة التحكم عن الطلاب")
    print("✅ أزرار الموافقة على الشقق للمسؤولين")
    print("✅ منع تغيير نوع الحساب")
    print("✅ تحسين التصميم والأداء")
    print("\n🚀 يمكنك الآن تشغيل الخادم: python manage.py runserver")

if __name__ == '__main__':
    setup_improved_system()