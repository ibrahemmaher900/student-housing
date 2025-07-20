import os
import django
import sys

# إعداد بيئة Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_housing.settings')
django.setup()

from django.contrib.auth.models import User
from apartments.models import SiteRating

def add_default_ratings():
    """إضافة تقييمات افتراضية للموقع"""
    
    # التأكد من وجود مستخدمين
    users = User.objects.all()[:3]
    if not users or users.count() < 3:
        print("لا يوجد مستخدمين كافيين. يرجى إنشاء مستخدمين أولاً.")
        return
    
    # إنشاء تقييمات افتراضية
    ratings_data = [
        {
            'user': users[0],
            'rating': 5,
            'review': "ساعدني موقع سكن طالب في العثور على شقة مناسبة قريبة من جامعتي بسعر معقول. الموقع سهل الاستخدام والتواصل مع المالك كان سلساً.",
            'is_approved': True
        },
        {
            'user': users[1],
            'rating': 4,
            'review': "وفرت الكثير من الوقت والجهد في البحث عن سكن. الصور والمعلومات المتوفرة على الموقع دقيقة جداً وساعدتني في اتخاذ القرار المناسب.",
            'is_approved': True
        },
        {
            'user': users[2],
            'rating': 5,
            'review': "كمالك عقار، ساعدني الموقع في تأجير شقتي بسرعة لطلاب جادين. النظام سهل الاستخدام والدعم الفني ممتاز.",
            'is_approved': True
        }
    ]
    
    # حفظ التقييمات
    for data in ratings_data:
        SiteRating.objects.get_or_create(
            user=data['user'],
            defaults={
                'rating': data['rating'],
                'review': data['review'],
                'is_approved': data['is_approved']
            }
        )
    
    print("تم إضافة التقييمات الافتراضية بنجاح!")

if __name__ == "__main__":
    add_default_ratings()