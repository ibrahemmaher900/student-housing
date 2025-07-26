# مشروع سكن طالب - دليل شامل

## نظرة عامة
موقع لإيجار السكن الطلابي يربط بين الطلاب ومالكي العقارات، مع نظام إدارة شامل ولوحات تحكم متقدمة.

## المميزات الرئيسية

### للطلاب:
- البحث عن السكن حسب الجامعة والسعر والمميزات
- حجز الشقق والغرف والأسرة
- نظام المفضلات
- التقييمات والتعليقات
- الإشعارات الفورية

### لمالكي العقارات:
- إضافة وإدارة العقارات
- لوحة تحكم شاملة
- إدارة الحجوزات
- نظام الإبلاغ عن المستخدمين غير الجادين

### للإدارة:
- لوحة تحكم إدارية متقدمة
- اعتماد/رفض العقارات
- إدارة المستخدمين
- إحصائيات شاملة

## البنية التقنية

### التطبيقات:
- `apartments/` - إدارة العقارات والحجوزات
- `users/` - إدارة المستخدمين والملفات الشخصية

### النماذج الرئيسية:
- `University` - الجامعات
- `Apartment` - العقارات
- `Booking` - الحجوزات
- `Rating` - التقييمات
- `Comment` - التعليقات
- `Notification` - الإشعارات
- `Profile` - الملفات الشخصية

## أوامر الإدارة

### إعداد البيانات الأولية:
```bash
python manage.py init_universities
python manage.py create_superuser --username admin --email admin@example.com --password admin123
python manage.py create_sample_data
```

### صيانة النظام:
```bash
python manage.py cleanup_data
python manage.py collectstatic
python manage.py migrate
```

## لوحات التحكم

### لوحة تحكم الأدمن:
- المسار: `/apartments/admin/dashboard/`
- المميزات:
  - إحصائيات شاملة
  - إدارة الشقق المعلقة
  - إدارة المستخدمين
  - الحجوزات الحديثة

### لوحة تحكم مالك العقار:
- المسار: `/apartments/owner/dashboard/`
- المميزات:
  - عرض جميع العقارات
  - إدارة الحجوزات
  - إحصائيات العقارات
  - إضافة عقارات جديدة

## نظام الأمان

### Middleware:
- `BannedUserMiddleware` - منع المستخدمين المحظورين
- `SecurityHeadersMiddleware` - إضافة headers الأمان

### التحقق من البيانات:
- `validators.py` - التحقق من الملفات والبيانات
- حماية من XSS و CSRF
- تشفير كلمات المرور

## إعدادات الإنتاج

### متغيرات البيئة:
```env
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://...
ALLOWED_HOSTS=yourdomain.com
DEBUG=False
```

### الملفات المطلوبة:
- `settings_production.py` - إعدادات الإنتاج
- `requirements.txt` - المتطلبات
- `Procfile` - إعدادات Render

## API Endpoints

### العقارات:
- `GET /apartments/` - قائمة العقارات
- `GET /apartments/<id>/` - تفاصيل العقار
- `POST /apartments/add/` - إضافة عقار

### الحجوزات:
- `POST /apartments/<id>/book/` - حجز عقار
- `GET /apartments/my-bookings/` - حجوزاتي
- `POST /apartments/booking/<id>/<status>/` - تحديث حالة الحجز

### الإشعارات:
- `GET /apartments/notifications/` - قائمة الإشعارات
- `GET /apartments/notifications/count/` - عدد الإشعارات
- `POST /apartments/notifications/<id>/read/` - تعليم كمقروء

## قاعدة البيانات

### الجداول الرئيسية:
- `apartments_university` - الجامعات
- `apartments_apartment` - العقارات
- `apartments_booking` - الحجوزات
- `apartments_rating` - التقييمات
- `apartments_comment` - التعليقات
- `apartments_notification` - الإشعارات
- `users_profile` - الملفات الشخصية

## التطوير والصيانة

### إضافة مميزات جديدة:
1. إنشاء النماذج في `models.py`
2. إنشاء الـ views في `views.py`
3. إضافة المسارات في `urls.py`
4. إنشاء القوالب في `templates/`

### اختبار النظام:
```bash
python manage.py test
python manage.py check
python manage.py runserver
```

## الأمان والحماية

### الحماية المطبقة:
- CSRF Protection
- XSS Protection
- SQL Injection Protection
- File Upload Security
- User Authentication
- Permission System

### التوصيات:
- استخدام HTTPS في الإنتاج
- تحديث Django بانتظام
- مراقبة السجلات
- نسخ احتياطية منتظمة

## الدعم والصيانة

### ملفات السجلات:
- `/tmp/django.log` - سجل التطبيق
- `security.log` - سجل الأمان

### المراقبة:
- مراقبة استخدام قاعدة البيانات
- مراقبة الذاكرة والمعالج
- مراقبة حركة المرور

## الخلاصة

المشروع مكتمل ويحتوي على جميع المميزات المطلوبة:
✅ لوحات تحكم للأدمن ومالك العقار
✅ نظام حجوزات متكامل
✅ نظام تقييمات وتعليقات
✅ نظام إشعارات
✅ أمان وحماية شاملة
✅ إدارة المستخدمين
✅ واجهة مستخدم متجاوبة