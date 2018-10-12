from datetime import datetime
from django.shortcuts import render
from .forms import WorkerInputForm

from AdminWorkspace.models import Catagory, Item


def home(request):
    """        General view for all user.    """
    return render(request, 'StaffWorkspace/home.html')


def input_form(request, catagory):
    """        Worker can input store related information.    """ 

    # As catagory is foreign key it will just store it's pk to Item table that's 
    #why we need to search both Catagory and Item table to get proper dynamic filtering.
    catagory = Catagory.objects.get(name=catagory)          # Collecting the name of catagory
    items = Item.objects.filter(catagory=catagory.id)       # Filtering item name from items using catagory.id

    context = {
        "form": WorkerInputForm,
        "items": items,
    }
    return render(request, 'StaffWorkspace/inputForm.html', context)


def worker_report(request):
    """        Report generation for worker.    """
    stock_item = [1, "10/10/2018", 121, "Book", "IUBAT", "Uttara", 20, 2000, 10, "05/10/2018", 5000,
             "MasTrade", "Very good"]
    context = {
        "date": datetime.now(),
        "stock_items": stock_item
    }
    return render(request, 'StaffWorkspace/workerReport.html', context)

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
    context = {
        "date": datetime.now(),
    }
    return render(request, 'StaffWorkspace/workerReport.html', context)


def worker_report_print(request):
    """        Report print for worker.    """
    return render(request, 'StaffWorkspace/workerReportPrint.html')
