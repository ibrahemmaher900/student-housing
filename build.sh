#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Python version: $(python --version)"
echo "Current directory: $(pwd)"

# Install all dependencies
pip install django>=4.2,<4.3
pip install django-allauth>=0.54.0
pip install django-environ>=0.10.0
pip install whitenoise>=6.4.0
pip install pillow>=9.5.0
pip install gunicorn>=21.2.0
pip install dj-database-url>=2.0.0
pip install django-cors-headers>=4.0.0
pip install django-csp>=3.7
pip install django-axes>=6.0.0
pip install requests>=2.31.0
pip install PyJWT>=2.0,<3.0
pip install cryptography>=41.0.0
pip install oauthlib>=3.2.0
pip install python3-openid>=3.2.0
pip install requests-oauthlib>=1.3.0

# Collect static files
python manage.py collectstatic --noinput

# Apply migrations
python manage.py migrate

# Create superuser
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
            print(f'Created apartment: {data[\"title\"]}')
        except Exception as e:
            print(f'Error creating apartment: {e}')
else:
    print(f'Using existing apartments: {Apartment.objects.count()}')
" || echo "Failed to create sample data"

echo "Build completed"
