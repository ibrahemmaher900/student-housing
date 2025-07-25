#!/usr/bin/env python3
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_housing.settings')
django.setup()

from django.core.cache import cache

# مسح جميع الكاش
cache.clear()
print("✅ تم مسح جميع الكاش")