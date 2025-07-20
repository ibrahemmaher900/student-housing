#!/usr/bin/env python
"""
سكريبت لإضافة بيانات افتراضية للشقق
"""
import os
import sys
import django
import random
from decimal import Decimal

# إعداد Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_housing.settings')
django.setup()

from django.contrib.auth.models import User
from django.db import transaction
from apartments.models import Apartment, University
from users.models import Profile

def create_sample_apartments():
    """إنشاء شقق افتراضية للعرض"""
    print("جاري إنشاء شقق افتراضية...")
    
    # التحقق من وجود جامعات
    universities = list(University.objects.all())
    if not universities:
        print("لا توجد جامعات، جاري إنشاء جامعات افتراضية...")
        universities = [
            University.objects.create(name="جامعة القاهرة", city="القاهرة"),
            University.objects.create(name="جامعة عين شمس", city="القاهرة"),
            University.objects.create(name="جامعة الإسكندرية", city="الإسكندرية"),
        ]
    
    # التحقق من وجود مستخدمين من نوع مالك
    owners = User.objects.filter(profile__user_type='owner')
    if not owners:
        print("لا يوجد مالكين، جاري إنشاء مستخدم مالك افتراضي...")
        owner = User.objects.create_user(
            username="owner1",
            email="owner1@example.com",
            password="password123",
            first_name="مالك",
            last_name="عقار"
        )
        Profile.objects.filter(user=owner).update(user_type='owner')
        owners = [owner]
    
    # إنشاء شقق افتراضية
    apartments_data = [
        {
            "title": "شقة فاخرة قرب جامعة القاهرة",
            "description": "شقة مفروشة بالكامل قريبة من الجامعة، مناسبة للطلاب",
            "price": Decimal("2500.00"),
            "deposit": Decimal("2500.00"),
            "city": "القاهرة",
            "district": "الجيزة",
            "address": "شارع الجامعة، الجيزة",
            "rooms": 3,
            "area": Decimal("120.00"),
            "floor": 2,
            "furnished": True,
            "gender": "mixed",
            "payment_method": "monthly",
            "bills_included": True,
            "available": True,
            "university": universities[0],
            "owner": owners[0],
            "contact_name": "أحمد محمد",
            "phone": "01012345678",
            "whatsapp_available": True,
            "advertiser_type": "owner",
            "has_wifi": True,
            "has_ac": True,
            "has_fridge": True,
            "has_washer": True,
            "has_kitchen": True,
            "has_private_bathroom": True,
            "apartment_type": "apartment"
        },
        {
            "title": "غرفة مشتركة قرب جامعة عين شمس",
            "description": "غرفة في شقة مشتركة، مناسبة للطالبات",
            "price": Decimal("1200.00"),
            "deposit": Decimal("1200.00"),
            "city": "القاهرة",
            "district": "مدينة نصر",
            "address": "شارع الألفي، مدينة نصر",
            "rooms": 1,
            "area": Decimal("20.00"),
            "floor": 3,
            "furnished": True,
            "gender": "female",
            "payment_method": "monthly",
            "bills_included": True,
            "available": True,
            "university": universities[1],
            "owner": owners[0],
            "contact_name": "سارة أحمد",
            "phone": "01098765432",
            "whatsapp_available": True,
            "advertiser_type": "owner",
            "has_wifi": True,
            "has_ac": False,
            "has_fridge": True,
            "has_washer": True,
            "has_kitchen": True,
            "has_private_bathroom": False,
            "apartment_type": "room"
        },
        {
            "title": "شقة مفروشة في الإسكندرية",
            "description": "شقة مفروشة بالكامل قريبة من جامعة الإسكندرية",
            "price": Decimal("3000.00"),
            "deposit": Decimal("3000.00"),
            "city": "الإسكندرية",
            "district": "سموحة",
            "address": "شارع فوزي معاذ، سموحة",
            "rooms": 2,
            "area": Decimal("90.00"),
            "floor": 1,
            "furnished": True,
            "gender": "male",
            "payment_method": "monthly",
            "bills_included": False,
            "available": True,
            "university": universities[2],
            "owner": owners[0],
            "contact_name": "محمد علي",
            "phone": "01234567890",
            "whatsapp_available": True,
            "advertiser_type": "owner",
            "has_wifi": True,
            "has_ac": True,
            "has_fridge": True,
            "has_washer": True,
            "has_kitchen": True,
            "has_private_bathroom": True,
            "apartment_type": "apartment"
        }
    ]
    
    # إنشاء الشقق
    created_count = 0
    for data in apartments_data:
        try:
            with transaction.atomic():
                # التحقق من وجود الشقة
                if not Apartment.objects.filter(title=data["title"], owner=data["owner"]).exists():
                    apartment = Apartment.objects.create(**data)
                    created_count += 1
                    print(f"تم إنشاء شقة: {apartment.title}")
        except Exception as e:
            print(f"خطأ في إنشاء شقة: {e}")
    
    print(f"تم إنشاء {created_count} شقق افتراضية")

if __name__ == "__main__":
    create_sample_apartments()