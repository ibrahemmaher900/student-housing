from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Apartment, ApartmentImage, University
from .forms import ApartmentForm

@login_required
def add_room(request):
    """إضافة غرفة جديدة"""
    # الحصول على قائمة الجامعات
    universities = University.objects.all()
    
    if request.method == 'POST':
        try:
            # معالجة الحقول المنطقية
            furnished = request.POST.get('furnished') == 'yes'
            has_wifi = request.POST.get('has_wifi') == 'on'
            has_ac = request.POST.get('has_ac') == 'on'
            has_kitchen = request.POST.get('has_kitchen') == 'on'
            has_washer = request.POST.get('has_washer') == 'on'
            has_fridge = request.POST.get('has_fridge') == 'on'
            has_private_bathroom = request.POST.get('has_private_bathroom') == 'yes'
            has_balcony = request.POST.get('has_balcony') == 'on'
            has_parking = False  # غير متوفر عادة في الغرف
            whatsapp_available = request.POST.get('whatsapp_available') == 'yes'
            bills_included = request.POST.get('bills_included') == 'yes'
            
            # معالجة القيم الرقمية
            try:
                price = float(request.POST.get('price', 0))
            except (ValueError, TypeError):
                price = 0
                
            try:
                distance_to_university = float(request.POST.get('distance_to_university', 0))
            except (ValueError, TypeError):
                distance_to_university = 0
                
            try:
                deposit = float(request.POST.get('deposit', 0))
            except (ValueError, TypeError):
                deposit = 0
                
            try:
                walking_time = int(request.POST.get('walking_time') or 0)
                if walking_time <= 0:
                    walking_time = None
            except (ValueError, TypeError):
                walking_time = None
                
            try:
                driving_time = int(request.POST.get('driving_time') or 0)
                if driving_time <= 0:
                    driving_time = None
            except (ValueError, TypeError):
                driving_time = None
                
            # معالجة الإحداثيات
            try:
                latitude = float(request.POST.get('latitude') or 0)
                if latitude == 0:
                    latitude = None
            except (ValueError, TypeError):
                latitude = None
                
            try:
                longitude = float(request.POST.get('longitude') or 0)
                if longitude == 0:
                    longitude = None
            except (ValueError, TypeError):
                longitude = None
            
            # إنشاء عنوان مناسب
            city = request.POST.get('city', '')
            district = request.POST.get('district', '')
            title = f"غرفة في {district}, {city}"
            
            # إنشاء غرفة جديدة
            apartment = Apartment(
                title=title,
                description=request.POST.get('additional_description', ''),
                price=price,
                apartment_type='room',
                area=float(request.POST.get('area', 0)),
                bedrooms=1,  # غرفة واحدة
                bathrooms=1 if has_private_bathroom else 0,
                address=request.POST.get('address', ''),
                latitude=latitude,
                longitude=longitude,
                distance_to_university=distance_to_university,
                walking_time=walking_time,
                driving_time=driving_time,
                university_id=request.POST.get('university'),
                owner=request.user,
                status='pending',
                furnished=furnished,
                has_wifi=has_wifi,
                has_ac=has_ac,
                has_kitchen=has_kitchen,
                has_washer=has_washer,
                has_fridge=has_fridge,
                has_private_bathroom=has_private_bathroom,
                has_balcony=has_balcony,
                has_parking=has_parking,
                max_people=int(request.POST.get('max_people', 1) or 1),
                floor=int(request.POST.get('floor', 0) or 0),
                conditions=request.POST.get('conditions', ''),
                additional_description=request.POST.get('additional_description', ''),
                contact_name=request.POST.get('contact_name', ''),
                phone=request.POST.get('phone', ''),
                whatsapp_available=whatsapp_available,
                advertiser_type=request.POST.get('advertiser_type', 'owner'),
                additional_contact=request.POST.get('additional_contact', ''),
                google_maps_link=request.POST.get('google_maps_link', ''),
                gender=request.POST.get('gender', 'all'),
                payment_method=request.POST.get('payment_method', 'monthly'),
                deposit=deposit,
                bills_included=bills_included,
                available=True
            )
            apartment.save()
            
            # حفظ الصور
            images = request.FILES.getlist('images')
            for image in images:
                ApartmentImage.objects.create(apartment=apartment, image=image)
            
            # إرسال إشعار للمسؤولين
            from django.contrib.auth.models import User
            from .models import Notification
            admins = User.objects.filter(is_staff=True) | User.objects.filter(is_superuser=True)
            for admin in admins:
                Notification.objects.create(
                    user=admin,
                    notification_type='apartment_pending',
                    message=f'تم إضافة غرفة جديدة "{apartment.title}" بواسطة {request.user.username} وتحتاج إلى موافقة',
                    related_apartment=apartment
                )
            
            # إظهار رسالة نجاح
            messages.success(request, 'تم إضافة الغرفة بنجاح! سيتم نشرها بعد مراجعتها من قبل الإدارة.')
            return redirect('my_apartments')
            
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            messages.error(request, 'حدث خطأ أثناء إضافة الغرفة. الرجاء المحاولة مرة أخرى.')
    
    return render(request, 'apartments/add_room.html', {'universities': universities})

@login_required
def add_bed(request):
    """إضافة سرير في غرفة مشتركة"""
    # الحصول على قائمة الجامعات
    universities = University.objects.all()
    
    if request.method == 'POST':
        try:
            # معالجة الحقول المنطقية
            furnished = request.POST.get('furnished') == 'yes'
            has_wifi = request.POST.get('has_wifi') == 'on'
            has_ac = request.POST.get('has_ac') == 'on'
            has_kitchen = request.POST.get('has_kitchen') == 'on'
            has_washer = request.POST.get('has_washer') == 'on'
            has_fridge = request.POST.get('has_fridge') == 'on'
            has_private_bathroom = request.POST.get('has_private_bathroom') == 'yes'
            has_balcony = False  # غير متوفر عادة في الأسرّة المشتركة
            has_parking = False  # غير متوفر عادة في الأسرّة المشتركة
            whatsapp_available = request.POST.get('whatsapp_available') == 'yes'
            bills_included = request.POST.get('bills_included') == 'yes'
            
            # معالجة القيم الرقمية
            try:
                price = float(request.POST.get('price', 0))
            except (ValueError, TypeError):
                price = 0
                
            try:
                distance_to_university = float(request.POST.get('distance_to_university', 0))
            except (ValueError, TypeError):
                distance_to_university = 0
                
            try:
                deposit = float(request.POST.get('deposit', 0))
            except (ValueError, TypeError):
                deposit = 0
                
            try:
                walking_time = int(request.POST.get('walking_time') or 0)
                if walking_time <= 0:
                    walking_time = None
            except (ValueError, TypeError):
                walking_time = None
                
            try:
                driving_time = int(request.POST.get('driving_time') or 0)
                if driving_time <= 0:
                    driving_time = None
            except (ValueError, TypeError):
                driving_time = None
                
            # معالجة الإحداثيات
            try:
                latitude = float(request.POST.get('latitude') or 0)
                if latitude == 0:
                    latitude = None
            except (ValueError, TypeError):
                latitude = None
                
            try:
                longitude = float(request.POST.get('longitude') or 0)
                if longitude == 0:
                    longitude = None
            except (ValueError, TypeError):
                longitude = None
            
            # إنشاء عنوان مناسب
            city = request.POST.get('city', '')
            district = request.POST.get('district', '')
            title = f"سرير مشترك في {district}, {city}"
            
            # إنشاء سرير جديد
            apartment = Apartment(
                title=title,
                description=request.POST.get('additional_description', ''),
                price=price,
                apartment_type='bed',
                area=float(request.POST.get('area', 0)),
                bedrooms=1,  # غرفة واحدة
                bathrooms=1 if has_private_bathroom else 0,
                address=request.POST.get('address', ''),
                latitude=latitude,
                longitude=longitude,
                distance_to_university=distance_to_university,
                walking_time=walking_time,
                driving_time=driving_time,
                university_id=request.POST.get('university'),
                owner=request.user,
                status='pending',
                furnished=furnished,
                has_wifi=has_wifi,
                has_ac=has_ac,
                has_kitchen=has_kitchen,
                has_washer=has_washer,
                has_fridge=has_fridge,
                has_private_bathroom=has_private_bathroom,
                has_balcony=has_balcony,
                has_parking=has_parking,
                max_people=1,  # سرير واحد = شخص واحد
                floor=int(request.POST.get('floor', 0) or 0),
                conditions=request.POST.get('conditions', ''),
                additional_description=request.POST.get('additional_description', ''),
                contact_name=request.POST.get('contact_name', ''),
                phone=request.POST.get('phone', ''),
                whatsapp_available=whatsapp_available,
                advertiser_type=request.POST.get('advertiser_type', 'owner'),
                additional_contact=request.POST.get('additional_contact', ''),
                google_maps_link=request.POST.get('google_maps_link', ''),
                gender=request.POST.get('gender', 'all'),
                payment_method=request.POST.get('payment_method', 'monthly'),
                deposit=deposit,
                bills_included=bills_included,
                available=True
            )
            apartment.save()
            
            # حفظ الصور
            images = request.FILES.getlist('images')
            for image in images:
                ApartmentImage.objects.create(apartment=apartment, image=image)
            
            # إرسال إشعار للمسؤولين
            from django.contrib.auth.models import User
            from .models import Notification
            admins = User.objects.filter(is_staff=True) | User.objects.filter(is_superuser=True)
            for admin in admins:
                Notification.objects.create(
                    user=admin,
                    notification_type='apartment_pending',
                    message=f'تم إضافة سرير مشترك جديد "{apartment.title}" بواسطة {request.user.username} ويحتاج إلى موافقة',
                    related_apartment=apartment
                )
            
            # إظهار رسالة نجاح
            messages.success(request, 'تم إضافة السرير المشترك بنجاح! سيتم نشره بعد مراجعته من قبل الإدارة.')
            return redirect('my_apartments')
            
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            messages.error(request, 'حدث خطأ أثناء إضافة السرير المشترك. الرجاء المحاولة مرة أخرى.')
    
    return render(request, 'apartments/add_bed.html', {'universities': universities})