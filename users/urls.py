from django.urls import path
from .views_auth_pro import login_pro, register_pro, logout_pro

urlpatterns = [
    path('login/', login_pro, name='login'),
    path('logout/', logout_pro, name='logout'),
    path('register/', register_pro, name='register'),
]
