from django import forms
from .models import Reservation, Client, VehicleType, Service, Location
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



class ReservationForm(forms.ModelForm):
    services = forms.ModelMultipleChoiceField(queryset=Service.objects.all(), widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Reservation
        fields = ['date', 'time_slot', 'reservation_type', 'vehicle_type', 'location']
        widgets = {
            'vehicle_type': forms.Select(attrs={'class': 'form-control'}),
            'services': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'location': forms.Select(attrs={'class': 'form-control'}),
        }


    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time_slot = cleaned_data.get('time_slot')
        reservation_type = cleaned_data.get('reservation_type')

        if date is None:
            raise ValidationError("Data nie może być pusta.")

        # Sprawdzenie, czy termin jest już zajęty
        if Reservation.objects.filter(date=date, time_slot=time_slot, reservation_type=reservation_type).exists():
            raise ValidationError("Wybrany termin jest już zajęty.")

        # Sprawdzenie, czy termin rezerwacji nie jest w przeszłości
        if date < timezone.now().date():
            raise ValidationError("Nie można rezerwować terminu w przeszłości.")

        # Walidacja określonych godzin dla rezerwacji (np. 8:00-18:00)
        if not (timezone.datetime.strptime('08:00', '%H:%M').time() <= time_slot <= timezone.datetime.strptime('18:00', '%H:%M').time()):
            raise ValidationError("Rezerwacje są możliwe tylko między 8:00 a 18:00.")

        return cleaned_data



class ClientRegistrationForm(UserCreationForm):
    company_name = forms.CharField(max_length=255)
    phone_number = forms.CharField(max_length=15)
    address = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            client = Client(user=user, company_name=self.cleaned_data['company_name'],
                            phone_number=self.cleaned_data['phone_number'], address=self.cleaned_data['address'])
            client.save()
        return user