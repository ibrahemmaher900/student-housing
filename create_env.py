#!/usr/bin/env python
"""
سكريبت لإنشاء ملف .env على Render
"""
import os
import secrets

def create_env_file():
    """إنشاء ملف .env على Render"""
    print("جاري إنشاء ملف .env...")
    
    # التحقق من وجود ملف .env
    if os.path.exists('.env'):
        print("ملف .env موجود بالفعل")
        return
    
    # إنشاء مفتاح سري عشوائي
    secret_key = secrets.token_urlsafe(50)
    
    # محتوى ملف .env
    env_content = f"""# .env file for Render
DJANGO_SECRET_KEY={secret_key}
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=.onrender.com,localhost,127.0.0.1
"""
    
    # كتابة الملف
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("تم إنشاء ملف .env بنجاح")

if __name__ == "__main__":
    create_env_file()