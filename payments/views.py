from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from bookings.models import Booking
from .forms import PaymentForm


@login_required
def payment_create_view(request, booking_id):
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        customer__user=request.user
    )

    if hasattr(booking, 'payment'):
        return redirect('booking_detail', booking_id=booking.id)

    if request.method == 'POST':
        form = PaymentForm(request.POST)

        if form.is_valid():
            payment = form.save(commit=False)
            payment.booking = booking
            payment.amount = booking.total_price
            payment.payment_status = 'paid'
            payment.save()

            booking.status = 'confirmed'
            booking.save()

            return redirect('booking_detail', booking_id=booking.id)
    else:
        form = PaymentForm()

    return render(request, 'payments/payment_form.html', {
        'form': form,
        'booking': booking
    })
