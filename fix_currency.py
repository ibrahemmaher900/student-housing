#!/usr/bin/env python
import os
import django
import glob

# إعداد Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_housing.settings')
django.setup()

# تغيير العملة في ملفات القوالب
template_files = glob.glob('templates/apartments/*.html')
for file_path in template_files:
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # استبدال ر.س بـ ج.م
    content = content.replace('ر.س', 'ج.م')
    content = content.replace('ريال', 'جنيه')
    content = content.replace('SAR', 'EGP')
    
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
    
    print(f"Updated currency in {file_path}")

print("Currency fix completed")
