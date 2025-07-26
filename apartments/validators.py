import os
import magic
from django.core.exceptions import ValidationError

def validate_file_type(upload):
    """
    التحقق من نوع الملف المرفوع للتأكد من أنه آمن
    """
    # الحصول على نوع MIME للملف
    file_type = magic.from_buffer(upload.read(1024), mime=True)
    # إعادة مؤشر الملف إلى البداية
    upload.seek(0)
    
    # قائمة أنواع الملفات المسموح بها
    allowed_types = [
        'image/jpeg',
        'image/png',
        'image/gif',
        'application/pdf',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    ]
    
    if file_type not in allowed_types:
        raise ValidationError(f'نوع الملف غير مسموح به. الأنواع المسموح بها هي: {", ".join(allowed_types)}')

def validate_file_size(upload):
    """
    التحقق من حجم الملف المرفوع
    """
    # الحد الأقصى لحجم الملف (5 ميجابايت)
    max_size = 5 * 1024 * 1024
    
    if upload.size > max_size:
        raise ValidationError('حجم الملف يتجاوز الحد المسموح به (5 ميجابايت)')

def validate_file_extension(upload):
    """
    التحقق من امتداد الملف المرفوع
    """
    ext = os.path.splitext(upload.name)[1]
    allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.pdf', '.doc', '.docx']
    
    if not ext.lower() in allowed_extensions:
        raise ValidationError(f'امتداد الملف غير مسموح به. الامتدادات المسموح بها هي: {", ".join(allowed_extensions)}')

def validate_file(upload):
    """
    دالة شاملة للتحقق من الملف المرفوع
    """
    validate_file_extension(upload)
    validate_file_size(upload)
    validate_file_type(upload)

def validate_phone_number(value):
    """التحقق من صحة رقم الهاتف المصري"""
    import re
    if not value:
        return
    pattern = r'^(\+20|0)?1[0125]\d{8}$'
    if not re.match(pattern, value):
        raise ValidationError('رقم الهاتف غير صحيح. يجب أن يكون رقم هاتف مصري صحيح.')

def validate_price(value):
    """التحقق من صحة السعر"""
    if value <= 0:
        raise ValidationError('السعر يجب أن يكون أكبر من صفر.')
    if value > 100000:
        raise ValidationError('السعر مرتفع جداً. يجب أن يكون أقل من 100,000 جنيه.')

def validate_area(value):
    """التحقق من صحة المساحة"""
    if value <= 0:
        raise ValidationError('المساحة يجب أن تكون أكبر من صفر.')
    if value > 1000:
        raise ValidationError('المساحة كبيرة جداً. يجب أن تكون أقل من 1000 متر مربع.')

def validate_coordinates(latitude, longitude):
    """التحقق من صحة الإحداثيات"""
    if latitude and longitude:
        if not (-90 <= latitude <= 90):
            raise ValidationError('خط العرض يجب أن يكون بين -90 و 90.')
        if not (-180 <= longitude <= 180):
            raise ValidationError('خط الطول يجب أن يكون بين -180 و 180.')

def validate_rating(value):
    """التحقق من صحة التقييم"""
    if not (1 <= value <= 5):
        raise ValidationError('التقييم يجب أن يكون بين 1 و 5 نجوم.')