from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from users.models import Profile

class Command(BaseCommand):
    help = 'Fix missing user profiles'

    def handle(self, *args, **options):
        self.stdout.write('🔧 إصلاح البروفايلات المفقودة...')
        
        fixed_count = 0
        for user in User.objects.all():
            if not hasattr(user, 'profile'):
                try:
                    Profile.objects.create(user=user)
                    self.stdout.write(f'✅ تم إنشاء بروفايل للمستخدم: {user.username}')
                    fixed_count += 1
                except Exception as e:
                    self.stdout.write(f'❌ خطأ في إنشاء بروفايل للمستخدم {user.username}: {e}')
        
        self.stdout.write(f'✅ تم إصلاح {fixed_count} بروفايل')