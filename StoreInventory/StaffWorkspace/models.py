from django.db import models
from django.contrib import admin
from AdminWorkspace.models import Item, StockLocation, Vendor


class Report(models.Model):
    date = models.DateField(auto_now_add=True)
    item_no = models.IntegerField()
    item_name = models.ForeignKey(Item, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    stock_location = models.ForeignKey(StockLocation, on_delete=models.CASCADE)
    cost_per_unit = models.FloatField(blank=True, null=True)
    previous_balance = models.FloatField()
    purchase = models.FloatField(blank=True, null=True)
    issued = models.FloatField(blank=True, null=True)
    ending_balance = models.FloatField(blank=True, null=True)
    issued_to = models.CharField(max_length=100, blank=True, null=True)
    comments = models.CharField(max_length=100, blank=True, null=True)
    added_by = models.CharField(max_length=500, blank=True, null=True)

    
class ReportAdmin(admin.ModelAdmin):
        """ This class is made for custom admin design in Report tab. """
        list_display = ('date', 'item_no', 'item_name','vendor', 
                        'stock_location', 'cost_per_unit',
                        'previous_balance', 'purchase', 'issued',
                        'ending_balance', 'issued_to', 'comments',)
        search_fields = ( 'item_no',)