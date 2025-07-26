from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from users.models import Profile

class Command(BaseCommand):
    help = 'إنشاء مستخدم أدمن'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='اسم المستخدم')
        parser.add_argument('--email', type=str, help='البريد الإلكتروني')
        parser.add_argument('--password', type=str, help='كلمة المرور')

    def handle(self, *args, **options):
        username = options.get('username') or 'admin'
        email = options.get('email') or 'admin@example.com'
        password = options.get('password') or 'admin123'

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'المستخدم {username} موجود بالفعل')
            )
            return

        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )

        # إنشاء البروفيل
        profile, created = Profile.objects.get_or_create(
            user=user,
            defaults={'user_type': 'owner'}
        )

        self.stdout.write(
            self.style.SUCCESS(f'تم إنشاء المستخدم الأدمن: {username}')
        )
        self.stdout.write(f'البريد الإلكتروني: {email}')
        self.stdout.write(f'كلمة المرور: {password}')