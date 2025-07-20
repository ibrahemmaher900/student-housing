#!/usr/bin/env bash
# exit on error
set -o errexit

# Print environment information
echo "Python version:"
python --version
echo "Current directory: $(pwd)"

# Install dependencies
pip install -r requirements.txt

# Create SQLite database
echo "Creating SQLite database..."
python manage.py makemigrations
python manage.py migrate

# Create superuser
echo "Creating superuser..."
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_housing.settings')
import django
django.setup()
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created')
else:
    print('Superuser already exists')
"

# Create sample data
echo "Creating sample data..."
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_housing.settings')
import django
django.setup()
from django.contrib.auth.models import User
from apartments.models import University, Apartment
from users.models import Profile
from decimal import Decimal

# Create universities
if University.objects.count() == 0:
    print('Creating universities...')
    universities = [
        University.objects.create(name='جامعة القاهرة', city='القاهرة'),
        University.objects.create(name='جامعة عين شمس', city='القاهرة'),
        University.objects.create(name='جامعة الإسكندرية', city='الإسكندرية')
    ]
else:
    universities = list(University.objects.all())
    print(f'Using existing universities: {len(universities)}')

# Create owner
owner = User.objects.filter(username='owner').first()
if not owner:
    print('Creating owner user...')
    owner = User.objects.create_user('owner', 'owner@example.com', 'password123')
    Profile.objects.filter(user=owner).update(user_type='owner')

# Create apartments
if Apartment.objects.count() == 0:
    print('Creating apartments...')
    apartments = [
        {
            'title': 'شقة فاخرة قرب جامعة القاهرة',
            'description': 'شقة مفروشة بالكامل قريبة من الجامعة، مناسبة للطلاب',
            'price': Decimal('2500.00'),
            'deposit': Decimal('2500.00'),
            'city': 'القاهرة',
            'district': 'الجيزة',
            'address': 'شارع الجامعة، الجيزة',
            'rooms': 3,
            'area': Decimal('120.00'),
            'floor': 2,
            'furnished': True,
            'gender': 'mixed',
            'payment_method': 'monthly',
            'bills_included': True,
            'available': True,
            'university': universities[0],
            'owner': owner,
            'contact_name': 'أحمد محمد',
            'phone': '01012345678',
            'whatsapp_available': True,
            'advertiser_type': 'owner',
            'has_wifi': True,
            'has_ac': True,
            'has_fridge': True,
            'has_washer': True,
            'has_kitchen': True,
            'has_private_bathroom': True,
            'apartment_type': 'apartment'
        },
        {
            'title': 'غرفة مشتركة قرب جامعة عين شمس',
            'description': 'غرفة في شقة مشتركة، مناسبة للطالبات',
            'price': Decimal('1200.00'),
            'deposit': Decimal('1200.00'),
            'city': 'القاهرة',
            'district': 'مدينة نصر',
            'address': 'شارع الألفي، مدينة نصر',
            'rooms': 1,
            'area': Decimal('20.00'),
            'floor': 3,
            'furnished': True,
            'gender': 'female',
            'payment_method': 'monthly',
            'bills_included': True,
            'available': True,
            'university': universities[1],
            'owner': owner,
            'contact_name': 'سارة أحمد',
            'phone': '01098765432',
            'whatsapp_available': True,
            'advertiser_type': 'owner',
            'has_wifi': True,
            'has_ac': False,
            'has_fridge': True,
            'has_washer': True,
            'has_kitchen': True,
            'has_private_bathroom': False,
            'apartment_type': 'room'
        }
    ]
    
    for data in apartments:
        Apartment.objects.create(**data)
        print(f'Created apartment: {data[\"title\"]}')
else:
    print(f'Using existing apartments: {Apartment.objects.count()}')
"

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Build completed successfully"