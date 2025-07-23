from django.urls import path
from . import views
from .views_login_fix import login_view_fixed
from .views_register_fix import register_fixed

urlpatterns = [
    path('login/', login_view_fixed, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', register_fixed, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/<str:username>/', views.view_profile, name='view_profile'),
]
