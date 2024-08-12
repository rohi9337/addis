from django.contrib import admin
from .models import Place
from .models import Booking
admin.site.register(Place)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'place', 'check_in_date', 'check_out_date', 'created_at')
    list_filter = ('check_in_date', 'check_out_date')
    search_fields = ('user__email', 'place__name')
    ordering = ('-check_in_date',)

