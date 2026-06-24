from django.db import models
from bookings.models import Booking


class Payment(models.Model):
    METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('bank_transfer', 'Bank Transfer'),
    ]

    STATUS_CHOICES = [
        ('paid', 'Paid'),
        ('unpaid', 'Unpaid'),
        ('refunded', 'Refunded'),
    ]

    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name='payment'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=30, choices=METHOD_CHOICES)
    payment_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='paid'
    )
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Payment for Booking #{self.booking.id}'
