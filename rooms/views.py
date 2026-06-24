from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from .models import Room
from .forms import RoomForm


def room_list_view(request):
    rooms = Room.objects.select_related('room_type').all()

    status = request.GET.get('status')
    search = request.GET.get('search')

    if status:
        rooms = rooms.filter(status=status)

    if search:
        rooms = rooms.filter(
            Q(room_number__icontains=search) |
            Q(room_type__name__icontains=search)
        )

    return render(request, 'rooms/room_list.html', {
        'rooms': rooms,
        'search': search,
    })


def room_detail_view(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    return render(request, 'rooms/room_detail.html', {
        'room': room
    })


@user_passes_test(lambda user: user.is_staff)
def room_create_view(request):
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('room_list')
    else:
        form = RoomForm()

    return render(request, 'rooms/room_form.html', {
        'form': form
    })
