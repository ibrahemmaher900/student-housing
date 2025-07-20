#!/bin/bash

# هذا السكريبت يقوم بتهيئة وتشغيل الموقع في بيئة الإنتاج

# التأكد من وجود ملف .env
if [ ! -f .env ]; then
    echo "خطأ: ملف .env غير موجود. قم بإنشاء ملف .env بناءً على ملف .env.example"
    exit 1
fi

# تنشيط البيئة الافتراضية
source venv/bin/activate

# تثبيت المكتبات المطلوبة
pip install -r requirements.txt

# جمع الملفات الثابتة
python manage.py collectstatic --noinput

# تطبيق الترحيلات
python manage.py migrate --settings=student_housing.production

# تشغيل الخادم
gunicorn --bind 0.0.0.0:8000 student_housing.wsgi_production:application