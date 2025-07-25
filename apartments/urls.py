from django.urls import path
from . import views
from . import views_notifications

urlpatterns = [
    path('', views.apartment_list, name='apartment_list'),
    path('<int:pk>/', views.apartment_detail, name='apartment_detail'),
    path('<int:pk>/book/', views.book_apartment, name='book_apartment'),
    path('<int:pk>/wishlist/', views.toggle_wishlist, name='toggle_wishlist'),
    path('add/', views.add_apartment, name='add_apartment'),
    path('<int:pk>/edit/', views.edit_apartment, name='edit_apartment'),
    path('<int:pk>/delete/', views.delete_apartment, name='delete_apartment'),
    path('my-apartments/', views.my_apartments, name='my_apartments'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('my-wishlist/', views.my_wishlist, name='my_wishlist'),
    path('manage-bookings/', views.manage_bookings, name='manage_bookings'),
    path('booking/<int:pk>/<str:status>/', views.update_booking_status, name='update_booking_status'),
    
    path('notifications/', views_notifications.notifications_list, name='notifications_list'),
    path('notifications/<int:pk>/read/', views_notifications.mark_notification_as_read, name='mark_notification_as_read'),
    path('notifications/<int:pk>/delete/', views_notifications.delete_notification, name='delete_notification'),
    path('notifications/mark-all-read/', views_notifications.mark_all_read, name='mark_all_read'),
    path('notifications/count/', views_notifications.get_notifications_count, name='notifications_count'),
    path('notifications/recent/', views_notifications.get_recent_notifications, name='recent_notifications'),
    
    path('owner/dashboard/', views.owner_dashboard, name='owner_dashboard'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/apartments/', views.admin_apartments, name='admin_apartments'),
    path('admin/apartments/<int:pk>/approve/', views.approve_apartment, name='approve_apartment'),
    path('admin/apartments/<int:pk>/reject/', views.reject_apartment, name='reject_apartment'),
]
