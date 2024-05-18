import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client
from .models import Reservation, VehicleType, Location, Service
from django.contrib.auth import authenticate

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='12345')

@pytest.fixture
def login_user(client, user):
    client.login(username='testuser', password='12345')
    return client

@pytest.fixture
def authenticated_user(client):
    user = User.objects.create_user(username='testuser', email='test@example.com', password='12345')
    client.login(username='testuser', password='12345')
    return client




@pytest.mark.django_db
def test_custom_logout_redirects(client):
    response = client.get(reverse('logout'))
    assert response.status_code == 302
    assert response.url == '/'  # Sprawdzenie czy przekierowanie następuje na stronę główną


@pytest.mark.django_db
def test_index_view(client):
    response = client.get(reverse('index'))
    assert response.status_code == 200
    content = response.content.decode('utf-8')
    print(content)
    assert "Witaj na Stronie Slot Reservation App" in content

@pytest.mark.django_db
def test_index_view_template(client):
    response = client.get(reverse('index'))
    assert 'index.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_redirect_to_reserve_slot(client):
    response = client.get(reverse('reserve_slot'))
    assert response.status_code == 302  # Oczekiwane przekierowanie

@pytest.mark.django_db
def test_reserve_slot_get(login_user):
    response = login_user.get(reverse('reserve_slot'))
    assert response.status_code == 200
    print(response.content.decode('utf-8'))
    assert "Zarezerwuj" in response.content.decode('utf-8')  # Załóżmy, że formularz ma pole "Rezerwacja"

@pytest.mark.django_db
def test_reserve_slot_post(login_user):
    vehicle_type = VehicleType.objects.create(tonnage=3.5)
    location = Location.objects.create(name='Warehouse_1', address='123 Street', capacity=100)
    service = Service.objects.create(description='Storage', price=100, duration='01:00:00')

    data = {
        'date': '2024-05-17',
        'time_slot': '10:00',
        'reservation_type': 'load',
        'vehicle_type': vehicle_type.id,
        'location': location.id,
        'services': [service.id]
    }
    response = login_user.post(reverse('reserve_slot'), data)
    assert response.status_code == 302  # Oczekiwane przekierowanie
    assert Reservation.objects.count() == 1

@pytest.mark.django_db
def test_show_reserved_slot(login_user):
    vehicle_type = VehicleType.objects.create(tonnage=3.5)
    location = Location.objects.create(name='Warehouse_1', address='123 Street', capacity=100)
    reservation = Reservation.objects.create(date='2024-05-17', time_slot='10:00', reservation_type='load', vehicle_type=vehicle_type, location=location)

    response = login_user.get(reverse('show_reserved_slot'))
    assert response.status_code == 200
    assert "latest_reservation" in response.context


@pytest.mark.django_db
def test_show_reserved_slot_template(login_user):
    response = login_user.get(reverse('show_reserved_slot'))
    assert 'show_reserved_slot.html' in [t.name for t in response.templates]



@pytest.mark.django_db
def test_show_all_reserved_slots(login_user):
    response = login_user.get(reverse('all_slots'))
    assert response.status_code == 200
    assert "reserved_slots" in response.context


@pytest.mark.django_db
def test_show_all_reserved_slots_template(login_user):
    response = login_user.get(reverse('all_slots'))
    assert 'show_reserved_all_slots.html' in [t.name for t in response.templates]

@pytest.mark.django_db
def test_register_get(client):
    response = client.get(reverse('register'))
    assert response.status_code == 200
    print(response.content.decode('utf-8'))
    assert "Register" in response.content.decode('utf-8')  # Załóżmy, że formularz ma pole "Rejestracja"

@pytest.mark.django_db
def test_register_post(client):
    data = {
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password1': 'strongpassword123',
        'password2': 'strongpassword123',
        'company_name': 'New Company',
        'phone_number': '123456789',
        'address': '123 Street'
    }
    response = client.post(reverse('register'), data)
    assert response.status_code == 302  # Oczekiwane przekierowanie
    assert User.objects.count() == 1

