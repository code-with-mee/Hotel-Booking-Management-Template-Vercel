from django.urls import path
from .views import payment_create_view


urlpatterns = [
    path('create/<int:booking_id>/', payment_create_view, name='payment_create'),
]
