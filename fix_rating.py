#!/usr/bin/env python
import os
import django

# إعداد Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_housing.settings')
django.setup()

from apartments.models import SiteRating
from django.contrib.auth.models import User

# التحقق من وجود جدول التقييمات
try:
    ratings_count = SiteRating.objects.count()
    print(f"Found {ratings_count} ratings")
except Exception as e:
    print(f"Error checking ratings: {e}")
    # إنشاء جدول التقييمات إذا لم يكن موجودًا
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS apartments_siterating (
            id SERIAL PRIMARY KEY,
            rating INTEGER NOT NULL,
            comment TEXT,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            user_id INTEGER REFERENCES auth_user(id)
        );
        """)
        print("Created ratings table")

print("Rating fix completed")
