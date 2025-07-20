from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'phone_number', 'university')
    list_filter = ('user_type', 'university')
    search_fields = ('user__username', 'user__email', 'phone_number')

admin.site.register(Profile, ProfileAdmin)