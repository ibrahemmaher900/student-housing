from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apartments.models import University, Apartment, ApartmentImage
from users.models import Profile
import random

class Command(BaseCommand):
    help = 'إنشاء بيانات تجريبية للموقع'

    def handle(self, *args, **options):
        # إنشاء مستخدمين تجريبيين
        self.create_sample_users()
        
        # إنشاء شقق تجريبية
        self.create_sample_apartments()
        
        self.stdout.write(
            self.style.SUCCESS('تم إنشاء البيانات التجريبية بنجاح!')
        )

    def create_sample_users(self):
        """إنشاء مستخدمين تجريبيين"""
        # مالكي عقارات
        owners_data = [
            {'username': 'owner1', 'email': 'owner1@example.com', 'first_name': 'أحمد', 'last_name': 'محمد'},
            {'username': 'owner2', 'email': 'owner2@example.com', 'first_name': 'محمد', 'last_name': 'علي'},
            {'username': 'owner3', 'email': 'owner3@example.com', 'first_name': 'علي', 'last_name': 'أحمد'},
        ]
        
        for owner_data in owners_data:
            if not User.objects.filter(username=owner_data['username']).exists():
                user = User.objects.create_user(
                    username=owner_data['username'],
                    email=owner_data['email'],
                    password='password123',
                    first_name=owner_data['first_name'],
                    last_name=owner_data['last_name']
                )
                Profile.objects.create(user=user, user_type='owner')
                self.stdout.write(f'تم إنشاء مالك العقار: {user.username}')

        # طلاب
        students_data = [
            {'username': 'student1', 'email': 'student1@example.com', 'first_name': 'سارة', 'last_name': 'أحمد'},
            {'username': 'student2', 'email': 'student2@example.com', 'first_name': 'فاطمة', 'last_name': 'محمد'},
            {'username': 'student3', 'email': 'student3@example.com', 'first_name': 'عمر', 'last_name': 'علي'},
        ]
        
        for student_data in students_data:
            if not User.objects.filter(username=student_data['username']).exists():
                user = User.objects.create_user(
                    username=student_data['username'],
                    email=student_data['email'],
                    password='password123',
                    first_name=student_data['first_name'],
                    last_name=student_data['last_name']
                )
                Profile.objects.create(user=user, user_type='student')
                self.stdout.write(f'تم إنشاء الطالب: {user.username}')

    def create_sample_apartments(self):
        """إنشاء شقق تجريبية"""
        owners = User.objects.filter(profile__user_type='owner')
        universities = University.objects.all()
        
        if not owners.exists() or not universities.exists():
            self.stdout.write(
                self.style.WARNING('لا توجد مالكي عقارات أو جامعات لإنشاء الشقق')
            )
            return

        apartments_data = [
            {
                'title': 'شقة مفروشة قريبة من الجامعة',
                'description': 'شقة مفروشة بالكامل، تحتوي على غرفتين وصالة ومطبخ وحمام. قريبة جداً من الجامعة.',
                'price': 2500,
                'apartment_type': '2bhk',
                'area': 80,
                'bedrooms': 2,
                'bathrooms': 1,
                'address': 'شارع الجامعة، المدينة الجامعية',
                'distance_to_university': 0.5,
                'furnished': True,
                'has_wifi': True,
                'has_ac': True,
                'status': 'approved'
            },
            {
                'title': 'استوديو للطلاب',
                'description': 'استوديو مناسب للطلاب، يحتوي على جميع المرافق الأساسية.',
                'price': 1500,
                'apartment_type': 'studio',
                'area': 35,
                'bedrooms': 1,
                'bathrooms': 1,
                'address': 'شارع النيل، وسط البلد',
                'distance_to_university': 1.2,
                'furnished': True,
                'has_wifi': True,
                'has_ac': False,
                'status': 'approved'
            },
            {
                'title': 'غرفة في شقة مشتركة',
                'description': 'غرفة واسعة في شقة مشتركة مع طلاب آخرين. بيئة هادئة ومناسبة للدراسة.',
                'price': 800,
                'apartment_type': 'room',
                'area': 20,
                'bedrooms': 1,
                'bathrooms': 1,
                'address': 'شارع الطلبة، حي الجامعة',
                'distance_to_university': 0.8,
                'furnished': True,
                'has_wifi': True,
                'has_ac': True,
                'status': 'approved'
            }
        ]

        for i, apt_data in enumerate(apartments_data):
            owner = random.choice(owners)
            university = random.choice(universities)
            
            apartment = Apartment.objects.create(
                owner=owner,
                university=university,
                **apt_data
            )
            
            self.stdout.write(f'تم إنشاء الشقة: {apartment.title}')