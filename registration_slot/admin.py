from django.contrib import admin
from .models import Client, VehicleType, Reservation, Service, Location

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'phone_number', 'address')
    search_fields = ('company_name', 'user__username', 'user__email')
    raw_id_fields = ('user',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('user')
        return queryset


admin.site.register(VehicleType)

admin.site.register(Reservation)

admin.site.register(Service)

admin.site.register(Location)