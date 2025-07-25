from django.urls import path
from . import views
from . import views_notifications
from . import views_comments
from . import views_ratings
from . import views_housing
from . import views_non_serious
from . import views_users

urlpatterns = [
    path('', views.apartment_list, name='apartment_list'),
    path('<int:pk>/', views.apartment_detail, name='apartment_detail'),
    path('<int:pk>/book/', views.book_apartment, name='book_apartment'),
    path('<int:pk>/wishlist/', views.toggle_wishlist, name='toggle_wishlist'),
    path('add/', views.add_apartment, name='add_apartment'),
    path('add/room/', views_housing.add_room, name='add_room'),
    path('add/bed/', views_housing.add_bed, name='add_bed'),
    path('<int:pk>/edit/', views.edit_apartment, name='edit_apartment'),
    path('<int:pk>/delete/', views.delete_apartment, name='delete_apartment'),
    path('my-apartments/', views.my_apartments, name='my_apartments'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('my-wishlist/', views.my_wishlist, name='my_wishlist'),
    path('manage-bookings/', views.manage_bookings, name='manage_bookings'),
    path('booking/<int:pk>/<str:status>/', views.update_booking_status, name='update_booking_status'),
    # تم إزالة مسار الخريطة المستقلة
    
    # مسارات التنبيهات
    path('notifications/', views_notifications.notifications_list, name='notifications_list'),
    path('notifications/<int:pk>/read/', views_notifications.mark_notification_as_read, name='mark_notification_as_read'),
    path('notifications/<int:pk>/delete/', views_notifications.delete_notification, name='delete_notification'),
    path('notifications/mark-all-read/', views_notifications.mark_all_read, name='mark_all_read'),
    # مسارات API للتنبيهات
    path('notifications/count/', views_notifications.get_notifications_count, name='notifications_count'),
    path('notifications/recent/', views_notifications.get_recent_notifications, name='recent_notifications'),
    path('notifications/<int:pk>/read/api/', views_notifications.mark_notification_as_read_api, name='mark_notification_as_read_api'),
    
    # مسارات التعليقات
    path('<int:apartment_id>/comment/', views_comments.add_comment, name='add_comment'),
    path('comment/<int:comment_id>/edit/', views_comments.edit_comment, name='edit_comment'),
    path('comment/<int:comment_id>/delete/', views_comments.delete_comment, name='delete_comment'),
    path('comment/<int:comment_id>/reply/', views_comments.add_reply, name='add_reply'),
    path('comment/<int:comment_id>/approve/', views_comments.approve_comment, name='approve_comment'),
    path('comment/<int:comment_id>/reject/', views_comments.reject_comment, name='reject_comment'),
    
    # مسارات إدارة الشقق
    path('owner/dashboard/', views.owner_dashboard, name='owner_dashboard'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/apartments/', views.admin_apartments, name='admin_apartments'),
    path('admin/apartments/<int:pk>/approve/', views.approve_apartment, name='approve_apartment'),
    path('admin/apartments/<int:pk>/reject/', views.reject_apartment, name='reject_apartment'),
    
    # مسارات التقييمات
    path('<int:apartment_id>/rating/', views_ratings.add_rating, name='add_rating'),
    path('rating/<int:rating_id>/delete/', views_ratings.delete_rating, name='delete_rating'),
    path('rating/<int:rating_id>/approve/', views_ratings.approve_rating, name='approve_rating'),
    path('rating/<int:rating_id>/reject/', views_ratings.reject_rating, name='reject_rating'),
    
    # مسارات الإبلاغ عن المستخدمين غير الجادين
    path('booking/<int:booking_id>/report-non-serious/', views_non_serious.report_non_serious, name='report_non_serious'),
    path('admin/users/<int:user_id>/unban/', views_non_serious.unban_user, name='unban_user'),
    
    # مسارات إدارة المستخدمين
    path('admin/users/', views_users.admin_users, name='admin_users'),
]