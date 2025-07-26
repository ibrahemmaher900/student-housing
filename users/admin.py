from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'phone', 'city', 'is_banned', 'non_serious_reports')
    list_filter = ('user_type', 'is_banned', 'city')
    search_fields = ('user__username', 'user__email', 'phone', 'city')
    actions = ['ban_users', 'unban_users', 'reset_reports']
    
    def ban_users(self, request, queryset):
        queryset.update(is_banned=True)
        self.message_user(request, f'تم حظر {queryset.count()} مستخدم بنجاح')
    ban_users.short_description = 'حظر المستخدمين المحددين'
    
    def unban_users(self, request, queryset):
        queryset.update(is_banned=False, non_serious_reports=0)
        self.message_user(request, f'تم إلغاء حظر {queryset.count()} مستخدم بنجاح')
    unban_users.short_description = 'إلغاء حظر المستخدمين المحددين'
    
    def reset_reports(self, request, queryset):
        queryset.update(non_serious_reports=0)
        self.message_user(request, f'تم إعادة تعيين عداد البلاغات لـ {queryset.count()} مستخدم')
    reset_reports.short_description = 'إعادة تعيين عداد البلاغات'

admin.site.register(Profile, ProfileAdmin)