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