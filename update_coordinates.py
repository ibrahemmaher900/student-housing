#!/usr/bin/env python
import os
import django
import requests
import time

# إعداد Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_housing.settings')
django.setup()

from apartments.models import Apartment

def update_apartment_coordinates():
    """تحديث إحداثيات الشقق باستخدام TomTom API"""
    
    # مفتاح API لخرائط TomTom
    api_key = '7bpllxbhJJfYhMPF0WfVFzyVShKdQrpq'
    
    # الحصول على جميع الشقق التي ليس لها إحداثيات
    apartments = Apartment.objects.filter(latitude__isnull=True) | Apartment.objects.filter(longitude__isnull=True)
    
    print(f"تم العثور على {apartments.count()} شقة بدون إحداثيات")
    
    for apartment in apartments:
        # تكوين عنوان البحث
        search_query = f"{apartment.address}, {apartment.university.city}, مصر"
        
        # استعلام TomTom API
        url = f"https://api.tomtom.com/search/2/search/{search_query}.json"
        params = {
            'key': api_key,
            'limit': 1
        }
        
        try:
            response = requests.get(url, params=params)
            data = response.json()
            
            if data.get('results') and len(data['results']) > 0:
                result = data['results'][0]
                position = result.get('position', {})
                
                # تحديث إحداثيات الشقة
                apartment.latitude = position.get('lat')
                apartment.longitude = position.get('lon')
                apartment.save()
                
                print(f"تم تحديث إحداثيات الشقة: {apartment.title}")
                print(f"  العنوان: {search_query}")
                print(f"  الإحداثيات: {apartment.latitude}, {apartment.longitude}")
            else:
                print(f"لم يتم العثور على إحداثيات للشقة: {apartment.title}")
                print(f"  العنوان: {search_query}")
            
            # انتظار لتجنب تجاوز حدود API
            time.sleep(1)
            
        except Exception as e:
            print(f"حدث خطأ أثناء تحديث إحداثيات الشقة {apartment.title}: {str(e)}")
    
    print("تم الانتهاء من تحديث الإحداثيات")

if __name__ == "__main__":
    update_apartment_coordinates()