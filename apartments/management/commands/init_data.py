from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apartments.models import University, Apartment, ApartmentImage
from users.models import Profile
import random

class Command(BaseCommand):
    help = 'تهيئة البيانات الافتراضية للموقع'

    def handle(self, *args, **kwargs):
        self.stdout.write('بدء تهيئة البيانات...')
        self.create_universities()
        owner, student = self.create_users()
        self.create_apartments(owner, University.objects.all())
        self.stdout.write(self.style.SUCCESS('تم الانتهاء من تهيئة البيانات بنجاح!'))

    def create_universities(self):
        universities = [
            {'name': 'جامعة القاهرة', 'city': 'القاهرة', 'image': '/static/img/universities/cairo-university.jpg'},
            {'name': 'جامعة عين شمس', 'city': 'القاهرة', 'image': '/static/img/universities/ain-shams.jpg'},
            {'name': 'جامعة الإسكندرية', 'city': 'الإسكندرية', 'image': '/static/img/universities/alexandria.jpg'},
            {'name': 'جامعة المنصورة', 'city': 'المنصورة', 'image': '/static/img/universities/mansoura.jpg'},
            {'name': 'جامعة أسيوط', 'city': 'أسيوط', 'image': '/static/img/universities/assiut.jpg'},
        ]
        
        created_universities = []
        for uni_data in universities:
            uni, created = University.objects.get_or_create(
                name=uni_data['name'],
                defaults={
                    'city': uni_data['city'],
                    'image': uni_data['image']
                }
            )
            if not created and not uni.image:
                uni.image = uni_data['image']
                uni.save()
                
            created_universities.append(uni)
            if created:
                self.stdout.write(f"تم إنشاء جامعة: {uni.name}")
        
        return created_universities

    def create_users(self):
        # إنشاء مستخدم مالك
        owner, created = User.objects.get_or_create(
            username='owner1',
            defaults={
                'email': 'owner1@example.com',
                'first_name': 'أحمد',
                'last_name': 'محمد',
            }
        )
        if created:
            owner.set_password('password123')
            owner.save()
            owner.profile.user_type = 'owner'
            owner.profile.save()
            self.stdout.write("تم إنشاء مستخدم مالك")
        
        # إنشاء مستخدم طالب
        student, created = User.objects.get_or_create(
            username='student1',
            defaults={
                'email': 'student1@example.com',
                'first_name': 'خالد',
                'last_name': 'أحمد',
            }
        )
        if created:
            student.set_password('password123')
            student.save()
            student.profile.user_type = 'student'
            student.profile.save()
            self.stdout.write("تم إنشاء مستخدم طالب")
        
        return owner, student

    def create_apartments(self, owner, universities):
        apartment_types = ['studio', '1bhk', '2bhk', '3bhk', 'shared']
        
        for i in range(1, 11):
            university = random.choice(list(universities))
            apartment_type = random.choice(apartment_types)
            
            apartment, created = Apartment.objects.get_or_create(
                title=f"شقة {i} قريبة من {university.name}",
                defaults={
                    'description': f"شقة جميلة ومريحة قريبة من {university.name}. مناسبة للطلاب، تتميز بموقعها الهادئ والقريب من الجامعة والخدمات.",
                    'price': random.randint(2000, 10000),
                    'apartment_type': apartment_type,
                    'area': random.randint(50, 200),
                    'bedrooms': random.randint(1, 4),
                    'bathrooms': random.randint(1, 3),
                    'address': f"حي {random.choice(['النزهة', 'الروضة', 'العليا', 'الملز', 'السلامة'])}، {university.city}",
                    'distance_to_university': round(random.uniform(0.5, 5.0), 1),
                    'university': university,
                    'available': True,
                    'furnished': random.choice([True, False]),
                    'has_wifi': random.choice([True, False]),
                    'has_ac': random.choice([True, False]),
                    'has_parking': random.choice([True, False]),
                    'owner': owner,
                    'status': 'approved',
                    # الحقول الجديدة
                    'gender': random.choice(['male', 'female', 'all']),
                    'payment_method': random.choice(['monthly', 'quarterly', 'yearly']),
                    'deposit': random.randint(1000, 5000),
                    'bills_included': random.choice([True, False]),
                    'max_people': random.randint(1, 5),
                    'floor': random.randint(1, 10),
                    'conditions': "يجب الالتزام بقواعد السكن والهدوء",
                    'contact_name': owner.get_full_name() or owner.username,
                    'phone': f"01{random.randint(0, 2)}{random.randint(10000000, 99999999)}",
                    'whatsapp_available': random.choice([True, False]),
                    'advertiser_type': 'owner',
                    'has_fridge': random.choice([True, False]),
                    'has_washer': random.choice([True, False]),
                    'has_kitchen': random.choice([True, False]),
                    'has_private_bathroom': random.choice([True, False]),
                    'has_balcony': random.choice([True, False]),
                }
            )
            
            if created:
                self.stdout.write(f"تم إنشاء شقة: {apartment.title}")