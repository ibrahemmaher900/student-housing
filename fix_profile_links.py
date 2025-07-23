#!/usr/bin/env python
import os
import re

# قائمة بالملفات التي قد تحتوي على روابط profile
template_files = [
    'templates/base/base.html',
    'templates/base/notifications_dropdown.html',
    'templates/apartments/home.html',
    'templates/apartments/apartment_detail.html',
    'templates/apartments/my_apartments.html'
]

for file_path in template_files:
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # استبدال {% url 'profile' %} بـ /users/profile/
        modified_content = re.sub(r'{%\s*url\s+[\'"]profile[\'"]\s*%}', '/users/profile/', content)
        
        if modified_content != content:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(modified_content)
            print(f"تم تعديل {file_path}")
