#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Python version: $(python --version)"
echo "Current directory: $(pwd)"

# Install dependencies
pip install django django-allauth django-environ whitenoise pillow gunicorn dj-database-url django-cors-headers django-csp django-axes requests PyJWT cryptography oauthlib python3-openid requests-oauthlib psycopg2-binary

# Collect static files
python manage.py collectstatic --noinput

# Apply migrations
python manage.py migrate

# Create superuser if not exists
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
        }
    ]
    
    for data in apartments:
        try:
            Apartment.objects.create(**data)
            print(f'Created apartment: {data["title"]}')
        except Exception as e:
            print(f'Error creating apartment: {e}')
else:
    print(f'Using existing apartments: {Apartment.objects.count()}')
"

echo "Build completed"
