from django.urls import path
from .views_rating_fix import add_rating

urlpatterns = [
    path('add-rating/', add_rating, name='add_rating'),
]
