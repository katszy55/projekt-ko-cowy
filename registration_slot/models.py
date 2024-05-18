from django.db import models
from django.contrib.auth.models import User

#Model reprezentujący typy pojadów

class VehicleType(models.Model):
    TONNAGE_CHOICES = (
        (24.0, '24 tony'),
        (7.5, '7,5 tony'),
        (3.5, '3,5 tony'),
    )
    tonnage = models.FloatField(choices=TONNAGE_CHOICES, unique=True)

    def __str__(self):
        return f"{self.tonnage} tony"


#Model reprezentujący dostepne serwisy
class Service(models.Model):
    STORAGE = 'Storage'
    SORTING = 'Sorting'
    DELIVERY = 'Delivery'
    DESCRIPTIONS = [
        (STORAGE, 'Storage'),
        (SORTING, 'Sorting'),
        (DELIVERY, 'Delivery')
    ]

    description = models.CharField(max_length=100, choices=DESCRIPTIONS)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.DurationField()

    def __str__(self):
        return self.description

#Model reprezentujący dostepne lokalizacje
class Location(models.Model):
    WAREHOUSE_1 = 'Warehouse_1'
    Warehouse_2 = 'Warehouse_2'
    NAME = [
        (WAREHOUSE_1, 'Warehouse_1'),
        (Warehouse_2, 'Warehouse_2')
    ]

    name = models.CharField(max_length=100, choices=NAME)
    address = models.CharField(max_length=255)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return self.name

#Model reprezentujący formularz rezerwacji
class Reservation(models.Model):
    LOAD = 'load'
    UNLOAD = 'unload'
    RESERVATION_TYPES = [
        (LOAD, 'Load'),
        (UNLOAD, 'Unload'),
    ]

    date = models.DateField()
    time_slot = models.TimeField()
    reservation_type = models.CharField(max_length=100, choices=RESERVATION_TYPES, default=LOAD)
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE, default=1)
    services = models.ManyToManyField(Service)
    location = models.ForeignKey(Location, max_length=100, on_delete=models.CASCADE, default=1)

    class Meta:
        unique_together = ('date', 'time_slot', 'reservation_type')  # Zapewnia unikalność slotów

    def __str__(self):
        return f"{self.date} {self.time_slot} - {self.get_reservation_type_display()}"


#Model reprezentujący dane uzytkownika
class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.company_name
