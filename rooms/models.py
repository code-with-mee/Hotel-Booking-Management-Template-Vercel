from django.db import models


class RoomType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    max_guests = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Room(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('maintenance', 'Maintenance'),
    ]

    room_number = models.CharField(max_length=20, unique=True)
    room_type = models.ForeignKey(
        RoomType,
        on_delete=models.CASCADE,
        related_name='rooms'
    )
    floor = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available'
    )
    image = models.ImageField(
        upload_to='rooms/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.room_number
