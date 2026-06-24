from django.urls import path
from .views import room_list_view, room_detail_view, room_create_view


urlpatterns = [
    path('', room_list_view, name='room_list'),
    path('create/', room_create_view, name='room_create'),
    path('<int:room_id>/', room_detail_view, name='room_detail'),
]
