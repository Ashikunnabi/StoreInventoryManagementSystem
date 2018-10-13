from datetime import datetime
from django.shortcuts import render, redirect
from .forms import WorkerInputForm

from AdminWorkspace.models import Catagory, Item, StockLocation, Vendor
from .models import Report


def home(request):
    """        General view for all user.    """
    return render(request, 'StaffWorkspace/home.html')


def input_form(request, catagory):
    """        Worker can input store related information.    """ 

    # As catagory is foreign key it will just store it's pk to Item table that's 
    #why we need to search both Catagory and Item table to get proper dynamic filtering.
    catagory = Catagory.objects.get(name=catagory)          # Collecting the name of catagory
    items = Item.objects.filter(catagory=catagory.id)       # Filtering item name from items using catagory.id
    vendors = Vendor.objects.all()
    stock_locations = StockLocation.objects.all()

    context = {
        "form": WorkerInputForm,
        "items": items,
        "vendors": vendors,
        "stock_locations": stock_locations,
    }
    return render(request, 'StaffWorkspace/inputForm.html', context)


def input_form_submit(request):
    """ When form is submitted it will check and validate as wll as save data. """
    if request.method == "POST":    
        # If your request is post then only this conditon will run otherwise not.
        item_name = request.POST.get("item_name")   
        vendor = request.POST.get("vendor_name")     
        stock_location = request.POST.get("stock_location")     
        cost_per_unit = request.POST.get("cost_per_unit")     
        previous_balance = int(request.POST.get("previous_balance"))    
        purchase = request.POST.get("purchase")     
        issued = request.POST.get("issued")     
        ending_balance = request.POST.get("ending_balance")     
        issued_to = request.POST.get("issued_to")     
        comments = request.POST.get("comments")     
        added_by = request.POST.get("item_name")           
        #print(item_name, item_no, vendor, stock_location, cost_per_unit, previous_balance, issued, issued_to, ending_balance, comments)
        
        # Collecting the information of a full row/object from diffrent model/table.
        item_detail = Item.objects.get(name=item_name)
        vendor_detail = Vendor.objects.get(name=vendor)
        stock_detail = StockLocation.objects.get(name=stock_location)
        
        # Making a query to Report table to save data.
        report_save = Report( item_name = Item.objects.get(pk=item_detail.id), 
                    item_no = item_detail.item_no, 
                    vendor=Vendor.objects.get(pk=vendor_detail.id), 
                    stock_location=StockLocation.objects.get(pk=stock_detail.id),
                    cost_per_unit = cost_per_unit,
                    previous_balance=previous_balance,
                    purchase =  purchase,
                    issued =issued,
                    ending_balance = ending_balance,
                    issued_to = issued_to,
                    comments = comments,
                    added_by = added_by)
        report_save.save()
        
    return redirect('worker_report')
    

def worker_report(request, date=None, itemNo=None, itemName=None, vendor=None):
    """        Report generation for worker.    """
    value1 = request.POST.get('itemNo')  
    value2 = request.POST.get('itemName')  
    value3 = request.POST.get('vendor')  
    value4 = request.POST.get('date')  
    print(value1)
    print(value2)
    print(value3)
    print(value4)
    
    report = Report.objects.all()
    
    context = {
        "date": datetime.now(),
        "report": report,
    }
    return render(request, 'StaffWorkspace/workerReport.html', context)


def worker_report_print(request):
    """        Report print for worker.    """
    return render(request, 'StaffWorkspace/workerReportPrint.html')
