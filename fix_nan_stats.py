#!/usr/bin/env python
import os
import django

# إعداد Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_housing.settings')
django.setup()

from apartments.models import Apartment
from django.db.models import Count

# طباعة إحصائيات الشقق
total = Apartment.objects.count()
available = Apartment.objects.filter(available=True).count()
print(f"Total apartments: {total}")
print(f"Available apartments: {available}")

# تحقق من وجود قيم null في الحقول المهمة
null_fields = {}
for field in ['price', 'rooms', 'area', 'university', 'owner']:
    count = Apartment.objects.filter(**{f"{field}__isnull": True}).count()
    if count > 0:
        null_fields[field] = count
        print(f"Found {count} apartments with null {field}")

# إصلاح مشكلة NaN في الإحصائيات
if 'price' in null_fields:
    print("Fixing null prices...")
    Apartment.objects.filter(price__isnull=True).update(price=0)

if 'rooms' in null_fields:
    print("Fixing null rooms...")
    Apartment.objects.filter(rooms__isnull=True).update(rooms=0)

if 'area' in null_fields:
    print("Fixing null areas...")
    Apartment.objects.filter(area__isnull=True).update(area=0)

print("Fix completed")
