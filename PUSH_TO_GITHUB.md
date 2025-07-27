# رفع التغييرات إلى GitHub

## المشكلة:
مشكلة في مصادقة Git مع GitHub

## الحل:

### الطريقة الأولى - GitHub Desktop:
1. افتح GitHub Desktop
2. اختر المشروع student_housing
3. ستجد التغييرات التالية:
   - BACKUP_INFO.md (جديد)
   - restore_backup.sh (جديد)
   - جميع التحديثات السابقة
4. اكتب commit message: "إضافة نظام النسخ الاحتياطية والاستعادة"
5. اضغط Commit to main
6. اضغط Push origin

### الطريقة الثانية - Personal Access Token:
1. اذهب إلى GitHub.com > Settings > Developer settings > Personal access tokens
2. أنشئ token جديد
3. استخدم الأمر:
```bash
git remote set-url origin https://YOUR_TOKEN@github.com/ibrahemmaher900/student-housing.git
git push origin main
git push origin stable-backup
git push origin --tags
```

### الطريقة الثالثة - SSH:
```bash
git remote set-url origin git@github.com:ibrahemmaher900/student-housing.git
git push origin main
git push origin stable-backup
git push origin --tags
```

## التحقق من النجاح:
بعد الرفع، تأكد من وجود:
- ✅ Branch: main (آخر التحديثات)
- ✅ Branch: stable-backup (النسخة المحمية)
- ✅ Tag: v1.0-stable (النسخة المستقرة)

## الملفات المطلوب رفعها:
- BACKUP_INFO.md
- restore_backup.sh
- جميع التحديثات السابقة (16 ملف)

## بعد الرفع:
النسخة ستكون محمية على GitHub ويمكن الوصول إليها من أي مكان.