from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apartments.models import Apartment, Booking, Notification
from users.models import Profile
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'تنظيف البيانات القديمة والمكررة'

    def handle(self, *args, **options):
        # تنظيف الإشعارات القديمة (أكثر من 30 يوم)
        old_notifications = Notification.objects.filter(
            created_at__lt=datetime.now() - timedelta(days=30),
            is_read=True
        )
        deleted_notifications = old_notifications.count()
        old_notifications.delete()
        
        # تنظيف الحجوزات المرفوضة القديمة (أكثر من 60 يوم)
        old_bookings = Booking.objects.filter(
            status='rejected',
            created_at__lt=datetime.now() - timedelta(days=60)
        )
        deleted_bookings = old_bookings.count()
        old_bookings.delete()
        
        # إنشاء بروفيلات للمستخدمين الذين لا يملكون بروفيل
        users_without_profile = User.objects.filter(profile__isnull=True)
        created_profiles = 0
        for user in users_without_profile:
            Profile.objects.create(user=user)
            created_profiles += 1
        
        # تحديث عدد المشاهدات للشقق التي لا تحتوي على مشاهدات
        apartments_without_views = Apartment.objects.filter(views_count__isnull=True)
        apartments_without_views.update(views_count=0)
        updated_apartments = apartments_without_views.count()
        
        self.stdout.write(
            self.style.SUCCESS(f'تم حذف {deleted_notifications} إشعار قديم')
        )
        self.stdout.write(
            self.style.SUCCESS(f'تم حذف {deleted_bookings} حجز مرفوض قديم')
        )
        self.stdout.write(
            self.style.SUCCESS(f'تم إنشاء {created_profiles} بروفيل جديد')
        )
        self.stdout.write(
            self.style.SUCCESS(f'تم تحديث {updated_apartments} شقة')
        )
        self.stdout.write(
            self.style.SUCCESS('تم الانتهاء من تنظيف البيانات')
        )