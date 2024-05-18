from django.contrib.auth.decorators import login_required
from .forms import ReservationForm, ClientRegistrationForm, VehicleType
from .models import Reservation, Client, VehicleType, Service, Location
from itertools import groupby
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from datetime import date
from django.contrib.auth import logout
from django.contrib.auth import views as auth_views



def index(request):
    return render(request, 'index.html')  # Strona główna aplikacji


def redirect_to_reserve_slot(request):
    return HttpResponseRedirect(reverse('reserve_slot'))  # Przekierowanie do widokdu rezerwacji


@login_required
def reserve_slot(request): # Widok rezerwacji
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.save()

            # Zapisanie zarezerwowanych usług
            services = form.cleaned_data.get('services')
            reservation.services.set(services)

            location = form.cleaned_data.get('location')
            reservation.save()

            messages.success(request, 'Rezerwacja została pomyślnie zapisana.')
            return redirect('show_reserved_slot')  # Przekieruj do strony sukcesu
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = ReservationForm()

    return render(request, 'reserve_slot.html', {'form': form})

def custom_logout(request):
    logout(request)
    return redirect('/')  # Przekierowanie do strony głównej aplikacji


def show_reserved_slot(request):
    try:
        latest_reservation = Reservation.objects.latest('id')
    except Reservation.DoesNotExist:
        raise Http404("Nie ma żadnych zarezerwowanych slotów.")

    services = latest_reservation.services.all()
    location = latest_reservation.location

    return render(request, 'show_reserved_slot.html', {'latest_reservation': latest_reservation, 'services': services}) # Widok ostatniego zarezerwowanego slotu


#
# def show_all_reserved_slots(request):
#     reserved_slots = Reservation.objects.all().order_by('date', 'time_slot', 'reservation_type', 'vehicle_type')
#     return render(request, 'show_reserved_all_slots.html', {'reserved_slots': reserved_slots}) # widok wszystkich zarezerwowanych slotów

# def show_all_reserved_slots(request):
#     reserved_slots = Reservation.objects.all().order_by('date', 'time_slot', 'reservation_type', 'vehicle_type', 'location')
#
#     # Grupowanie zarezerwowanych slotów według lokalizacji
#     grouped_slots = {}
#     for location, slots in groupby(reserved_slots, key=lambda x: x.location):
#         grouped_slots[location] = list(slots)
#
#     return render(request, 'show_reserved_all_slots.html', {'grouped_slots': grouped_slots})



def show_all_reserved_slots(request): # Widok wszystkich zarezerwowanych slotów
    today = date.today()
    reserved_slots = Reservation.objects.filter(date__gte=today).order_by('date', 'time_slot', 'reservation_type', 'vehicle_type')
    return render(request, 'show_reserved_all_slots.html', {'reserved_slots': reserved_slots, 'today': today})


def register(request): # Widok rejestracji
    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Przekierowanie do strony logowania po pomyślnej rejestracji
    else:
        form = ClientRegistrationForm()
    return render(request, 'register.html', {'form': form})


def custom_password_reset(request):
    if request.method == 'POST':
        response = auth_views.PasswordResetView.as_view(
            template_name='password_reset.html',  # Twój własny szablon HTML dla formularza resetowania hasła
            # email_template_name='registration/password_reset_email.html',  # Szablon HTML dla wiadomości e-mail z linkiem resetowania hasła
            success_url=reverse('password_reset_confirm')  # Przekierowanie do widoku potwierdzenia po udanym wysłaniu e-maila z linkiem resetowania hasła
        )(request)
        return response
    return render(request, 'password_reset_form.html', {'background_color': '#ffffff'})  # Twój szablon formularza resetowania hasła




