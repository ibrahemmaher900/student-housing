#!/usr/bin/env python
"""
سكريبت لتعديل قالب base.html
"""
import os

# قراءة محتوى الملف
base_path = os.path.join('templates', 'base', 'base.html')
with open(base_path, 'r', encoding='utf-8') as file:
    content = file.read()

# البحث عن موقع القائمة الرئيسية
nav_items_start = content.find('<ul class="navbar-nav me-auto">')
if nav_items_start != -1:
    # البحث عن نهاية عناصر القائمة
    nav_items_end = content.find('</ul>', nav_items_start)
    
    # إضافة تضمين قالب owner_menu.html قبل نهاية عناصر القائمة
    owner_menu_include = '{% include "base/owner_menu.html" %}'
    
    # التحقق مما إذا كان التضمين موجودًا بالفعل
    if owner_menu_include not in content:
        new_content = content[:nav_items_end] + '\n        ' + owner_menu_include + '\n      ' + content[nav_items_end:]
        
        # كتابة المحتوى المعدل إلى الملف
        with open(base_path, 'w', encoding='utf-8') as file:
            file.write(new_content)
        
        print(f"تم تعديل {base_path} بنجاح")
    else:
        print(f"التضمين موجود بالفعل في {base_path}")
else:
    print(f"لم يتم العثور على القائمة الرئيسية في {base_path}")
