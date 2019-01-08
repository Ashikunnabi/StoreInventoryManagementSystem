from django.db import models
from django.contrib import admin


class Catagory(models.Model):
    name = models.CharField(max_length=20, unique=True)
    color = models.CharField(max_length=7)
    image = models.FileField(default=None, null=True)
    
    class Meta:
        verbose_name_plural = "categories"
    
    def __str__(self):
        return self.name
    
    
class Item(models.Model):
    name = models.CharField(max_length=100, unique=True)
    item_no = models.CharField(max_length=50, unique=True)
    balance = models.IntegerField()
    cost_per_unit = models.FloatField()
    safety_stock_limit = models.IntegerField()
    catagory = models.ForeignKey('Catagory', on_delete=models.CASCADE) # If Catagory is no more then related item will also auto deleted
                                                                       # as because on_delete=models.CASCADE
    
    def __str__(self):
        return self.name   
        
    
class ItemAdmin(admin.ModelAdmin):
        """ This class is made for custom admin design in Item tab. """
        list_display = ('item_no', 'name', 'catagory')
        list_filter = ('catagory',)
        search_fields = ( 'item_no',)
    
    
class Vendor(models.Model):
    name = models.CharField(max_length=100, unique=True)
    address = models.TextField()

    def __str__(self):
        return self.name    
    
class StockLocation(models.Model):
    name = models.CharField(max_length=20, unique=True)
    address = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
