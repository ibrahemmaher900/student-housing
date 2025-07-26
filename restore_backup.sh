#!/bin/bash

# سكريبت استعادة النسخة الاحتياطية

echo "🔄 بدء استعادة النسخة الاحتياطية المستقرة..."

# التحقق من وجود النسخة الاحتياطية
if [ -d "/Users/ibrahemmaher/student_housing_STABLE_BACKUP" ]; then
    echo "✅ تم العثور على النسخة الاحتياطية المحلية"
    
    # إنشاء نسخة احتياطية من الحالة الحالية
    echo "📦 إنشاء نسخة احتياطية من الحالة الحالية..."
    cp -r /Users/ibrahemmaher/student_housing /Users/ibrahemmaher/student_housing_CURRENT_BACKUP_$(date +%Y%m%d_%H%M%S)
    
    # استعادة النسخة المستقرة
    echo "🔄 استعادة النسخة المستقرة..."
    rm -rf /Users/ibrahemmaher/student_housing/*
    cp -r /Users/ibrahemmaher/student_housing_STABLE_BACKUP/* /Users/ibrahemmaher/student_housing/
    
    echo "✅ تم استعادة النسخة المستقرة بنجاح!"
    echo "📍 يمكنك الآن تشغيل الموقع بأمان"
    
else
    echo "❌ لم يتم العثور على النسخة الاحتياطية المحلية"
    echo "🔄 محاولة الاستعادة من Git..."
    
    cd /Users/ibrahemmaher/student_housing
    
    # التحقق من وجود tag
    if git tag | grep -q "v1.0-stable"; then
        echo "✅ تم العثور على Git tag"
        git checkout v1.0-stable
        echo "✅ تم استعادة النسخة من Git tag"
    elif git branch -r | grep -q "origin/stable-backup"; then
        echo "✅ تم العثور على stable branch"
        git checkout stable-backup
        echo "✅ تم استعادة النسخة من stable branch"
    else
        echo "❌ لم يتم العثور على أي نسخة احتياطية"
        echo "⚠️  يرجى التحقق من Git repository"
    fi
fi

echo "🎉 انتهت عملية الاستعادة"