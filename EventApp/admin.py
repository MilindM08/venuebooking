from django.contrib import admin
from.models import Venue,Booking,Rating,Order

# Register your models here.
class AdminVenue(admin.ModelAdmin):
    list_display=('vid','vname','location','capacity','price','image','state','desc')
    
admin.site.register(Venue,AdminVenue)    


class AdminBooking(admin.ModelAdmin):
    list_display=('bid','user','venue','date','status','is_completed','quantity')
    
admin.site.register(Booking,AdminBooking)  


class AdminRating(admin.ModelAdmin):
    list_display=('venue','user','score','comment','created_at')
    
admin.site.register(Rating,AdminRating) 


class OrdermAdmin(admin.ModelAdmin):
    list_display=('order_id','venue','quantity','user','date_added','is_completed') 
    
admin.site.register(Order,OrdermAdmin)


 