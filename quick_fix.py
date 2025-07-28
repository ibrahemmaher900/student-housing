#!/usr/bin/env python3
"""
إصلاح سريع للأزرار - تحويل إلى forms
"""

# إنشاء forms بسيطة للأزرار
admin_apartments_fix = '''
<!-- استبدال الأزرار بـ forms -->
<form method="post" action="{% url 'approve_apartment' apartment.id %}" style="display: inline;">
    {% csrf_token %}
    <button type="submit" class="btn btn-sm btn-success me-2" onclick="return confirm('هل أنت متأكد من اعتماد هذه الشقة؟')">
        <i class="fas fa-check me-1"></i> موافقة
    </button>
</form>
<form method="post" action="{% url 'reject_apartment' apartment.id %}" style="display: inline;">
    {% csrf_token %}
    <button type="submit" class="btn btn-sm btn-danger" onclick="return confirm('هل أنت متأكد من رفض هذه الشقة؟')">
        <i class="fas fa-times me-1"></i> رفض
    </button>
</form>
'''

owner_dashboard_fix = '''
<!-- استبدال الأزرار بـ forms -->
<form method="post" action="{% url 'update_booking_status' booking.id 'approve' %}" style="display: inline;">
    {% csrf_token %}
    <button type="submit" class="btn btn-sm btn-success" onclick="return confirm('هل أنت متأكد من قبول هذا الحجز؟')">قبول</button>
</form>
<form method="post" action="{% url 'update_booking_status' booking.id 'reject' %}" style="display: inline;">
    {% csrf_token %}
    <button type="submit" class="btn btn-sm btn-danger" onclick="return confirm('هل أنت متأكد من رفض هذا الحجز؟')">رفض</button>
</form>
'''

print("✅ الحل: استبدال الروابط بـ forms مع POST method")
print("📝 استخدم الكود أعلاه في الـ templates")
print("🔧 هذا سيحل مشكلة Method Not Allowed")