from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from rooms.models import Room
from .models import Booking
from .forms import BookingForm


@login_required
def booking_list_view(request):
    bookings = Booking.objects.filter(
        customer__user=request.user
    ).select_related('room', 'room__room_type')

    return render(request, 'bookings/booking_list.html', {
        'bookings': bookings
    })


@login_required
def booking_detail_view(request, booking_id):
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        customer__user=request.user
    )

    return render(request, 'bookings/booking_detail.html', {
        'booking': booking
    })


@login_required
def booking_create_view(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    if request.method == 'POST':
        form = BookingForm(request.POST, room=room)

        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user.customer_profile
            booking.room = room

            nights = (
                booking.check_out_date - booking.check_in_date
            ).days

            booking.total_price = room.room_type.price_per_night * nights
            booking.status = 'pending'
            booking.save()

            return redirect('booking_detail', booking_id=booking.id)
    else:
        form = BookingForm(room=room)

    return render(request, 'bookings/booking_form.html', {
        'form': form,
        'room': room
    })


@login_required
def booking_cancel_view(request, booking_id):
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        customer__user=request.user
    )

    booking.status = 'cancelled'
    booking.save()

    return redirect('booking_list')
