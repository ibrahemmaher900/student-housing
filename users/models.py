from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    USER_TYPE_CHOICES = [
        ('student', 'طالب'),
        ('owner', 'مالك عقار'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name="المستخدم")
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='student', verbose_name="نوع المستخدم")
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name="رقم الهاتف")
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name="المدينة")
    university = models.ForeignKey('apartments.University', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="الجامعة")
    bio = models.TextField(blank=True, null=True, verbose_name="نبذة شخصية")
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True, verbose_name="الصورة الشخصية")
    non_serious_reports = models.IntegerField(default=0, verbose_name="عدد الإبلاغات عن عدم الجدية")
    is_banned = models.BooleanField(default=False, verbose_name="محظور من الحجز")
    
    def get_profile_picture_url(self):
        """إرجاع رابط الصورة الشخصية أو الصورة الافتراضية حسب نوع المستخدم"""
        if self.profile_picture and hasattr(self.profile_picture, 'url') and self.profile_picture.name != 'profile_pics/default.png':
            return self.profile_picture.url
        
        # إرجاع صورة افتراضية من Bootstrap حسب نوع المستخدم
        if self.user_type == 'student':
            return "https://ui-avatars.com/api/?name=" + self.user.get_full_name().replace(" ", "+") + "&background=4e73df&color=ffffff&size=200"
        else:  # owner
            return "https://ui-avatars.com/api/?name=" + self.user.get_full_name().replace(" ", "+") + "&background=1cc88a&color=ffffff&size=200"
    
    def __str__(self):
        return f"ملف {self.user.username} الشخصي"
    
    class Meta:
        verbose_name = "الملف الشخصي"
        verbose_name_plural = "الملفات الشخصية"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        try:
            Profile.objects.get_or_create(user=instance)
        except:
            pass

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        if hasattr(instance, 'profile'):
            instance.profile.save()
        else:
            Profile.objects.get_or_create(user=instance)
    except:
        pass