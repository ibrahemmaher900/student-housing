from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apartments.views_fix import home_fixed

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_fixed, name='home'),  # استخدام الصفحة الرئيسية المعدلة
    path('apartments/', include('apartments.urls')),
    path('users/', include('users.urls')),
    path('accounts/', include('allauth.urls')),
]

# إضافة مسارات الملفات الثابتة والوسائط
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
