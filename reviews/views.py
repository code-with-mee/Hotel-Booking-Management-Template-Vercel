from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from bookings.models import Booking
from .forms import ReviewForm


@login_required
def review_create_view(request, booking_id):
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        customer__user=request.user
    )

    if hasattr(booking, 'review'):
        return redirect('booking_detail', booking_id=booking.id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.booking = booking
            review.customer = request.user.customer_profile
            review.save()

            return redirect('booking_detail', booking_id=booking.id)
    else:
        form = ReviewForm()

    return render(request, 'reviews/review_form.html', {
        'form': form,
        'booking': booking
    })
