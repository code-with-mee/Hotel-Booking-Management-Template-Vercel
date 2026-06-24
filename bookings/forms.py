from django import forms
from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'check_in_date',
            'check_out_date',
        ]

        widgets = {
            'check_in_date': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),
            'check_out_date': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),
        }

        labels = {
            'check_in_date': 'Check-in Date',
            'check_out_date': 'Check-out Date',
        }

    def __init__(self, *args, **kwargs):
        self.room = kwargs.pop('room', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        check_in_date = cleaned_data.get('check_in_date')
        check_out_date = cleaned_data.get('check_out_date')

        if check_in_date and check_out_date:
            if check_out_date <= check_in_date:
                raise forms.ValidationError(
                    'Check-out date must be after check-in date.'
                )

        if self.room and self.room.status != 'available':
            raise forms.ValidationError(
                'This room is not available.'
            )

        if self.room and check_in_date and check_out_date:
            conflict = Booking.objects.filter(
                room=self.room,
                check_in_date__lt=check_out_date,
                check_out_date__gt=check_in_date
            ).exclude(status='cancelled')

            if conflict.exists():
                raise forms.ValidationError(
                    'This room is already booked for the selected date.'
                )

        return cleaned_data
