from django.urls import path
from .views import (
    booking_list_view,
    booking_detail_view,
    booking_create_view,
    booking_cancel_view,
)


urlpatterns = [
    path('', booking_list_view, name='booking_list'),
    path('<int:booking_id>/', booking_detail_view, name='booking_detail'),
    path('create/<int:room_id>/', booking_create_view, name='booking_create'),
    path('<int:booking_id>/cancel/', booking_cancel_view, name='booking_cancel'),
]
