from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
class Room(models.Model):
    ROOM_TYPES = (
        ('single', 'Single'),
        ('double', 'Double'),
        ('suite', 'Suite'),
    )
    ROOM_STATUS = (
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('maintenance', 'Maintenance'),
    )
    
    number = models.CharField(max_length=10, unique=True)
    type = models.CharField(max_length=10, choices=ROOM_TYPES)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=ROOM_STATUS, default='available')

    def __str__(self):
        return f"Room {self.number} - {self.get_type_display()}"

    @classmethod
    def create_rooms(cls, num_rooms=100):
        for i in range(1, num_rooms + 1):
            room_type = cls.ROOM_TYPES[i % len(cls.ROOM_TYPES)][0]
            price = 100 + (i * 10)  # Simple price calculation
            cls.objects.create(number=f"Room{i:03d}", type=room_type, price=price)

    @classmethod
    def update_room_status(cls):
        current_date = timezone.now().date()
        occupied_rooms = cls.objects.filter(
            reservation__check_out__gt=current_date,
            reservation__check_in__lte=current_date
        ).distinct()
        
        for room in occupied_rooms:
            room.status = 'occupied'
            room.save()

        vacant_rooms = cls.objects.exclude(id__in=occupied_rooms)
        for room in vacant_rooms:
            room.status = 'available'
            room.save()

        return occupied_rooms.count(), vacant_rooms.count()
class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.name

class Reservation(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.customer.name} - Room {self.room.number} ({self.check_in} to {self.check_out})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        Room.update_room_status()