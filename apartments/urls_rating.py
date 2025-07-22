from django.urls import path
from .simple_rating_view import simple_rating

urlpatterns = [
    path('add-rating/', simple_rating, name='add_rating'),
]
