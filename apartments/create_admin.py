import os
import django

# إعداد Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_housing.settings')
django.setup()

from django.contrib.auth.models import User

def create_superuser():
    # التحقق من وجود مستخدم مسؤول
    if not User.objects.filter(is_superuser=True).exists():
        # إنشاء مستخدم مسؤول جديد
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123',
            first_name='مدير',
            last_name='النظام'
        )
        print("تم إنشاء مستخدم مسؤول بنجاح!")
        print("اسم المستخدم: admin")
        print("كلمة المرور: admin123")
    else:
        print("يوجد مستخدم مسؤول بالفعل")

if __name__ == "__main__":
    create_superuser()