from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apartments.views_safe import safe_home
from apartments.views_static import apartment_list, apartment_detail
from student_housing.error_handlers import handler400, handler403, handler404, handler500
from .debug import debug_view
from .health import health_check

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', safe_home, name='home'),  # Use safe home page that doesn't depend on database
    path('apartments/', apartment_list, name='apartment_list'),
    path('apartments/<int:apartment_id>/', apartment_detail, name='apartment_detail'),
    path('users/', include('users.urls')),
    path('accounts/', include('allauth.urls')),
    path('', include('apartments.urls_rating')),
    path('debug/', debug_view, name='debug'),
    path('health/', health_check, name='health'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # تعيين معالجات الأخطاء المخصصة
    handler400 = 'student_housing.error_handlers.handler400'
    handler403 = 'student_housing.error_handlers.handler403'
    handler404 = 'student_housing.error_handlers.handler404'
    handler500 = 'student_housing.error_handlers.handler500'