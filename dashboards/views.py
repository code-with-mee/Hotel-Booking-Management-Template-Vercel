from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from bookings.models import Booking
from payments.models import Payment
from reviews.models import Review


@login_required
def dashboard_view(request):
    bookings = Booking.objects.filter(customer__user=request.user)
    payments = Payment.objects.filter(booking__customer__user=request.user)
    reviews = Review.objects.filter(customer__user=request.user)

    total_paid_amount = payments.filter(
        payment_status='paid'
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0

    context = {
        'total_bookings': bookings.count(),
        'pending_bookings': bookings.filter(status='pending').count(),
        'confirmed_bookings': bookings.filter(status='confirmed').count(),
        'completed_bookings': bookings.filter(status='completed').count(),
        'total_payments': payments.count(),
        'total_paid_amount': total_paid_amount,
        'total_reviews': reviews.count(),
        'recent_bookings': bookings.order_by('-created_at')[:5],
    }

    return render(request, 'dashboards/dashboard.html', context)
