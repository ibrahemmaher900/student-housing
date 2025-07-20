from django.urls import path
from . import views_rating

urlpatterns = [
    path('submit-rating/', views_rating.submit_rating, name='submit_rating'),
]