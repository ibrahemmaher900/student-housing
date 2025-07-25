from django.urls import path
from .views_auth_pro import login_pro, register_pro, logout_pro
from . import views

urlpatterns = [
    path('login/', login_pro, name='login'),
    path('logout/', logout_pro, name='logout'),
    path('register/', register_pro, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/ajax/', views.profile_ajax, name='profile_ajax'),
    path('profile/<str:username>/', views.view_profile, name='view_profile'),
]
