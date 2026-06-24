from django.urls import path
from .views import review_create_view


urlpatterns = [
    path('create/<int:booking_id>/', review_create_view, name='review_create'),
]
