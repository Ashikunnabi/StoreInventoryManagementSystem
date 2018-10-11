from django.db import models


class Report(models.Model):
    serial_no = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    item_no = models.IntegerField()
    item_name = models.CharField(max_length=500)
    vendor = models.CharField(max_length=500)
    stock_location = models.CharField(max_length=500)
    cost_per_unit = models.FloatField()
    previous_balance = models.FloatField()
    purchase = models.FloatField()
    issued = models.DateField()
    ending_balance = models.FloatField()
    issued_to = models.CharField(max_length=500)
    comments = models.CharField(max_length=500)
    #added_by =
