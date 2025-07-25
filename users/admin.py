from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'phone', 'city')
    list_filter = ('user_type', 'is_banned')
    search_fields = ('user__username', 'user__email', 'phone')

admin.site.register(Profile, ProfileAdmin)