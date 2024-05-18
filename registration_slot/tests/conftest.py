import pytest
from registration_slot.models import Reservation, VehicleType, Location, Service

@pytest.fixture
def reservation():
    vehicle_type = VehicleType.objects.create(tonnage=24.0)
    location = Location.objects.create(name='Warehouse_1', address='123 Street', capacity=100)
    service = Service.objects.create(description='Storage', price=100, duration='01:00:00')
    return Reservation.objects.create(
        date='2024-05-18',
        time_slot='8:00',
        reservation_type='Load',
        vehicle_type=vehicle_type,
        location=location,
        services=service
    )
