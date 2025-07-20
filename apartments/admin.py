from django.contrib import admin
from .models import University, Apartment, ApartmentImage, Booking, Wishlist, Comment, Notification, Rating

class ApartmentImageInline(admin.TabularInline):
    model = ApartmentImage
    extra = 3

class ApartmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'apartment_type', 'university', 'status', 'available', 'owner', 'created_at')
    list_filter = ('status', 'available', 'apartment_type', 'university', 'furnished', 'has_wifi', 'has_ac')
    search_fields = ('title', 'description', 'address')
    inlines = [ApartmentImageInline]
    actions = ['approve_apartments', 'reject_apartments']
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'price', 'apartment_type', 'area', 'bedrooms', 'bathrooms', 'owner')
        }),
        ('الموقع', {
            'fields': ('address', 'latitude', 'longitude', 'university', 'distance_to_university')
        }),
        ('المميزات', {
            'fields': ('available', 'furnished', 'has_wifi', 'has_ac', 'has_parking')
        }),
        ('حالة الإعلان', {
            'fields': ('status',),
            'classes': ('wide',)
        }),
    )
    
    def approve_apartments(self, request, queryset):
        queryset.update(status='approved')
        self.message_user(request, f'تمت الموافقة على {queryset.count()} شقة بنجاح')
    approve_apartments.short_description = 'الموافقة على الشقق المحددة'
    
    def reject_apartments(self, request, queryset):
        queryset.update(status='rejected')
        self.message_user(request, f'تم رفض {queryset.count()} شقة بنجاح')
    reject_apartments.short_description = 'رفض الشقق المحددة'

class BookingAdmin(admin.ModelAdmin):
    list_display = ('apartment', 'student', 'start_date', 'end_date', 'status', 'created_at')
    list_filter = ('status', 'start_date')
    search_fields = ('apartment__title', 'student__username')

class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'apartment', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'apartment__title')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'apartment', 'content', 'created_at', 'is_approved')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('user__username', 'apartment__title', 'content')
    actions = ['approve_comments', 'reject_comments']
    
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f'تم اعتماد {queryset.count()} تعليق بنجاح')
    approve_comments.short_description = 'اعتماد التعليقات المحددة'
    
    def reject_comments(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(request, f'تم رفض {queryset.count()} تعليق بنجاح')
    reject_comments.short_description = 'رفض التعليقات المحددة'

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification_type', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('user__username', 'message')

class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'apartment', 'stars', 'created_at', 'is_approved')
    list_filter = ('stars', 'is_approved', 'created_at')
    search_fields = ('user__username', 'apartment__title', 'review')
    actions = ['approve_ratings', 'reject_ratings']
    
    def approve_ratings(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f'تم اعتماد {queryset.count()} تقييم بنجاح')
    approve_ratings.short_description = 'اعتماد التقييمات المحددة'
    
    def reject_ratings(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(request, f'تم رفض {queryset.count()} تقييم بنجاح')
    reject_ratings.short_description = 'رفض التقييمات المحددة'

admin.site.register(University)
admin.site.register(Apartment, ApartmentAdmin)
admin.site.register(ApartmentImage)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Rating, RatingAdmin)