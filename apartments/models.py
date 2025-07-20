from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class University(models.Model):
    name = models.CharField(max_length=100, verbose_name="اسم الجامعة")
    city = models.CharField(max_length=50, verbose_name="المدينة")
    image = models.CharField(max_length=255, blank=True, null=True, verbose_name="مسار الصورة")
    
    def __str__(self):
        return self.name
    
    def get_image_url(self):
        if self.image and self.image.startswith('/'):
            return self.image
        elif self.image:
            return f"/static/img/universities/{self.image}"
        return "/static/img/universities/default-university.jpg"
    
    class Meta:
        verbose_name = "جامعة"
        verbose_name_plural = "الجامعات"

class Apartment(models.Model):
    APARTMENT_TYPE_CHOICES = [
        ('studio', 'استوديو'),
        ('1bhk', 'غرفة وصالة'),
        ('2bhk', 'غرفتين وصالة'),
        ('3bhk', 'ثلاث غرف وصالة'),
        ('shared', 'سكن مشترك'),
        ('room', 'غرفة'),
        ('bed', 'سرير في مشاركة'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'بانتظار الموافقة'),
        ('approved', 'تمت الموافقة'),
        ('rejected', 'مرفوض'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('monthly', 'شهري'),
        ('quarterly', 'كل 3 شهور'),
        ('yearly', 'سنوي'),
    ]
    
    GENDER_CHOICES = [
        ('male', 'ذكور'),
        ('female', 'إناث'),
        ('all', 'الجميع'),
    ]
    
    ADVERTISER_TYPE_CHOICES = [
        ('owner', 'صاحب الشقة'),
        ('agent', 'وسيط / سمسار'),
    ]
    
    title = models.CharField(max_length=100, verbose_name="عنوان الإعلان")
    description = models.TextField(verbose_name="وصف الشقة")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="السعر الشهري")
    apartment_type = models.CharField(max_length=10, choices=APARTMENT_TYPE_CHOICES, verbose_name="نوع السكن")
    area = models.IntegerField(verbose_name="المساحة بالمتر المربع")
    bedrooms = models.IntegerField(verbose_name="عدد غرف النوم")
    bathrooms = models.IntegerField(verbose_name="عدد الحمامات")
    address = models.CharField(max_length=200, verbose_name="العنوان")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name="خط العرض")
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name="خط الطول")
    distance_to_university = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="المسافة للجامعة (كم)")
    walking_time = models.IntegerField(null=True, blank=True, verbose_name="الوقت مشياً (دقائق)")
    driving_time = models.IntegerField(null=True, blank=True, verbose_name="الوقت بالسيارة (دقائق)")
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name="apartments", verbose_name="الجامعة القريبة")
    available = models.BooleanField(default=True, verbose_name="متاح")
    furnished = models.BooleanField(default=False, verbose_name="مفروش")
    has_wifi = models.BooleanField(default=False, verbose_name="يوجد واي فاي")
    has_ac = models.BooleanField(default=False, verbose_name="يوجد تكييف")
    has_parking = models.BooleanField(default=False, verbose_name="يوجد موقف سيارات")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="apartments", verbose_name="المالك")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name="حالة الإعلان")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ النشر")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")
    
    # حقول إضافية
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='all', verbose_name="مخصص لـ")
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES, default='monthly', verbose_name="طريقة الدفع")
    deposit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="مبلغ التأمين")
    bills_included = models.BooleanField(default=False, verbose_name="تشمل الفواتير")
    max_people = models.IntegerField(null=True, blank=True, verbose_name="الحد الأقصى للأشخاص")
    floor = models.IntegerField(null=True, blank=True, verbose_name="الطابق")
    conditions = models.TextField(null=True, blank=True, verbose_name="شروط السكن")
    additional_description = models.TextField(null=True, blank=True, verbose_name="وصف إضافي")
    
    # بيانات الاتصال
    contact_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="اسم المعلن")
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name="رقم الهاتف")
    whatsapp_available = models.BooleanField(default=False, verbose_name="متاح على واتساب")
    advertiser_type = models.CharField(max_length=10, choices=ADVERTISER_TYPE_CHOICES, default='owner', verbose_name="نوع المعلن")
    additional_contact = models.TextField(null=True, blank=True, verbose_name="طرق تواصل إضافية")
    google_maps_link = models.URLField(null=True, blank=True, verbose_name="رابط خرائط جوجل")
    
    # مرافق إضافية
    has_fridge = models.BooleanField(default=False, verbose_name="يوجد ثلاجة")
    has_washer = models.BooleanField(default=False, verbose_name="يوجد غسالة")
    has_kitchen = models.BooleanField(default=False, verbose_name="يوجد مطبخ")
    has_private_bathroom = models.BooleanField(default=False, verbose_name="يوجد حمام خاص")
    has_balcony = models.BooleanField(default=False, verbose_name="يوجد بلكونة")
    
    # عدد المشاهدات
    views_count = models.PositiveIntegerField(default=0, verbose_name="عدد المشاهدات")
    
    def __str__(self):
        return self.title
    
    def get_average_rating(self):
        ratings = self.ratings.filter(is_approved=True)
        if ratings.exists():
            return round(sum(rating.stars for rating in ratings) / ratings.count(), 1)
        return 0
    
    def get_ratings_count(self):
        return self.ratings.filter(is_approved=True).count()
    
    def has_approved_booking(self):
        return self.bookings.filter(status='approved').exists()
    
    def get_approved_booking(self):
        return self.bookings.filter(status='approved').first()
    
    class Meta:
        verbose_name = "شقة"
        verbose_name_plural = "الشقق"
        ordering = ['-created_at']

class ApartmentImage(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name="images", verbose_name="الشقة")
    image = models.ImageField(upload_to='apartments/', verbose_name="الصورة")
    
    def __str__(self):
        return f"صورة لـ {self.apartment.title}"
    
    class Meta:
        verbose_name = "صورة الشقة"
        verbose_name_plural = "صور الشقق"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'قيد الانتظار'),
        ('approved', 'تمت الموافقة'),
        ('rejected', 'مرفوض'),
        ('cancelled', 'ملغي'),
        ('non_serious', 'غير جاد'),
    ]
    
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name="bookings", verbose_name="الشقة")
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings", verbose_name="الطالب")
    start_date = models.DateField(verbose_name="تاريخ البداية")
    end_date = models.DateField(verbose_name="تاريخ النهاية")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending', verbose_name="الحالة")
    message = models.TextField(blank=True, null=True, verbose_name="رسالة الطلب")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الطلب")
    
    def __str__(self):
        return f"حجز {self.apartment.title} بواسطة {self.student.username}"
    
    class Meta:
        verbose_name = "حجز"
        verbose_name_plural = "الحجوزات"
        ordering = ['-created_at']


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlists", verbose_name="المستخدم")
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name="wishlists", verbose_name="الشقة")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإضافة")
    
    def __str__(self):
        return f"{self.user.username} - {self.apartment.title}"
    
    class Meta:
        verbose_name = "مفضلة"
        verbose_name_plural = "المفضلات"
        unique_together = ('user', 'apartment')
        ordering = ['-created_at']


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('booking_request', 'طلب حجز'),
        ('booking_approved', 'تمت الموافقة على الحجز'),
        ('booking_rejected', 'تم رفض الحجز'),
        ('apartment_approved', 'تمت الموافقة على الشقة'),
        ('apartment_rejected', 'تم رفض الشقة'),
        ('apartment_pending', 'شقة جديدة بحاجة للموافقة'),
        ('new_comment', 'تعليق جديد'),
        ('comment_reply', 'رد على تعليق'),
        ('non_serious_booking', 'حجز غير جاد'),
        ('user_banned', 'تم حظر المستخدم'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications", verbose_name="المستخدم")
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, verbose_name="نوع التنبيه")
    message = models.TextField(verbose_name="الرسالة")
    related_booking = models.ForeignKey('Booking', on_delete=models.CASCADE, null=True, blank=True, related_name="notifications", verbose_name="الحجز المتعلق")
    related_apartment = models.ForeignKey('Apartment', on_delete=models.CASCADE, null=True, blank=True, related_name="notifications", verbose_name="الشقة المتعلقة")
    related_comment = models.ForeignKey('Comment', on_delete=models.CASCADE, null=True, blank=True, related_name="notifications", verbose_name="التعليق المتعلق")
    is_read = models.BooleanField(default=False, verbose_name="مقروء")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    
    def __str__(self):
        return f"{self.user.username} - {self.get_notification_type_display()} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
    
    class Meta:
        verbose_name = "تنبيه"
        verbose_name_plural = "التنبيهات"
        ordering = ['-created_at']


class Comment(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name="comments", verbose_name="الشقة")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments", verbose_name="المستخدم")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="replies", verbose_name="التعليق الأصلي")
    content = models.TextField(verbose_name="محتوى التعليق")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")
    is_approved = models.BooleanField(default=True, verbose_name="معتمد")
    
    def __str__(self):
        return f"تعليق بواسطة {self.user.username} على {self.apartment.title}"
    
    class Meta:
        verbose_name = "تعليق"
        verbose_name_plural = "التعليقات"
        ordering = ['-created_at']


class Rating(models.Model):
    RATING_CHOICES = [
        (1, '1 - سيء جداً'),
        (2, '2 - سيء'),
        (3, '3 - متوسط'),
        (4, '4 - جيد'),
        (5, '5 - ممتاز'),
    ]
    
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name="ratings", verbose_name="الشقة")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ratings", verbose_name="المستخدم")
    stars = models.IntegerField(choices=RATING_CHOICES, verbose_name="التقييم")
    review = models.TextField(verbose_name="المراجعة", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")
    is_approved = models.BooleanField(default=True, verbose_name="معتمد")
    
    def __str__(self):
        return f"تقييم {self.stars} نجوم بواسطة {self.user.username} لـ {self.apartment.title}"
    
    class Meta:
        verbose_name = "تقييم"
        verbose_name_plural = "التقييمات"
        ordering = ['-created_at']
        unique_together = ('user', 'apartment')  # لضمان أن كل مستخدم يقيم الشقة مرة واحدة فقط

class SiteRating(models.Model):
    RATING_CHOICES = [
        (1, '1 - سيء جداً'),
        (2, '2 - سيء'),
        (3, '3 - متوسط'),
        (4, '4 - جيد'),
        (5, '5 - ممتاز'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="site_ratings", verbose_name="المستخدم")
    rating = models.IntegerField(choices=RATING_CHOICES, verbose_name="التقييم")
    review = models.TextField(blank=True, null=True, verbose_name="الرأي")
    is_approved = models.BooleanField(default=False, verbose_name="معتمد")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    
    def __str__(self):
        return f"تقييم {self.rating} نجوم بواسطة {self.user.username}"
    
    class Meta:
        verbose_name = "تقييم الموقع"
        verbose_name_plural = "تقييمات الموقع"
        ordering = ['-created_at']