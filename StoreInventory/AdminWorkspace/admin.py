from django.contrib import admin
from .models import Catagory, Item, Vendor, StockLocation, ItemAdmin


admin.site.site_title = 'Mas Trade International Garments Ltd.'
admin.site.index_title = 'Admin'
admin.site.site_header = 'Mas Trade International Garments Ltd.'
        
           
admin.site.register(Catagory)
admin.site.register(Item, ItemAdmin)
admin.site.register(Vendor)
admin.site.register(StockLocation)
