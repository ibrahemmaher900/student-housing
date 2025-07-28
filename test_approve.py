#!/usr/bin/env python3
"""
اختبار زر الموافقة على الشقة
"""

print("🔍 فحص زر الموافقة على الشقة...")

# فحص الـ view
with open('apartments/views.py', 'r') as f:
    views_content = f.read()

print("\n📋 فحص approve_apartment view:")
if '@login_required' in views_content and '@user_passes_test(is_admin)' in views_content:
    print("✅ Decorators موجودة")
else:
    print("❌ Decorators مفقودة")

if "def approve_apartment(request, pk):" in views_content:
    print("✅ Function موجودة")
else:
    print("❌ Function مفقودة")

if "apartment.status = 'approved'" in views_content:
    print("✅ Status update موجود")
else:
    print("❌ Status update مفقود")

if "Notification.objects.create" in views_content:
    print("✅ Notification creation موجود")
else:
    print("❌ Notification creation مفقود")

# فحص الـ template
with open('templates/apartments/admin_apartments.html', 'r') as f:
    template_content = f.read()

print("\n📋 فحص admin_apartments template:")
if '<form method="post"' in template_content:
    print("✅ POST forms موجودة")
else:
    print("❌ POST forms مفقودة")

if '{% csrf_token %}' in template_content:
    print("✅ CSRF tokens موجودة")
else:
    print("❌ CSRF tokens مفقودة")

if 'approve_apartment' in template_content:
    print("✅ approve_apartment URL موجود")
else:
    print("❌ approve_apartment URL مفقود")

# فحص الـ URLs
with open('apartments/urls.py', 'r') as f:
    urls_content = f.read()

print("\n📋 فحص URLs:")
if 'approve_apartment' in urls_content:
    print("✅ approve_apartment URL pattern موجود")
else:
    print("❌ approve_apartment URL pattern مفقود")

print("\n🎯 التشخيص:")
print("إذا كانت جميع الفحوصات ✅، فالمشكلة قد تكون:")
print("1. عدم تسجيل الدخول كمسؤول")
print("2. مشكلة في قاعدة البيانات")
print("3. خطأ في JavaScript")
print("4. مشكلة في الخادم")

print("\n🔧 الحلول المقترحة:")
print("1. تأكد من تسجيل الدخول كمسؤول")
print("2. تحقق من console في المتصفح")
print("3. تحقق من server logs")
print("4. جرب بدون JavaScript (إزالة onclick)")