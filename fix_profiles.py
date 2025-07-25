#!/usr/bin/env python3
"""
إصلاح البروفايلات المفقودة
"""

import os
import sys
import django

# إعداد Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_housing.settings')
django.setup()

from django.contrib.auth.models import User
from users.models import Profile

def fix_profiles():
    """إنشاء بروفايلات للمستخدمين المفقودة"""
    print("🔧 إصلاح البروفايلات المفقودة...")
    
    users_without_profile = []
    for user in User.objects.all():
        if not hasattr(user, 'profile'):
            users_without_profile.append(user)
    
    print(f"📊 عدد المستخدمين بدون بروفايل: {len(users_without_profile)}")
    
    for user in users_without_profile:
        try:
            Profile.objects.create(user=user)
            print(f"✅ تم إنشاء بروفايل للمستخدم: {user.username}")
        except Exception as e:
            print(f"❌ خطأ في إنشاء بروفايل للمستخدم {user.username}: {e}")
    
    print("✅ انتهى إصلاح البروفايلات")

if __name__ == '__main__':
    fix_profiles()