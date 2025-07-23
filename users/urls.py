from django.urls import path
from . import views
from .views_simple_logout import simple_logout

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', simple_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/<str:username>/', views.view_profile, name='view_profile'),
]
