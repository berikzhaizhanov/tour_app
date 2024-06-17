from django.contrib import admin
from .models import Member, Tour, Hotel, OrderHotel,Comment,Reservation,ReservationHotel
from .models import OrderTour, Customer

# Register your models here.
admin.site.register(Tour)
admin.site.register(Customer)
admin.site.register(OrderTour)
admin.site.register(Hotel)
admin.site.register(OrderHotel)
admin.site.register(Comment)
admin.site.register(Reservation)
admin.site.register(ReservationHotel)