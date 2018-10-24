from django.contrib.auth import authenticate, login, logout
from datetime import datetime, date
from django.shortcuts import render, redirect
from .forms import WorkerInputForm
from .models import Report

from AdminWorkspace.models import Catagory, Item, StockLocation, Vendor

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            context={
                "error": "Please put valid username / password."
            }            
            return render(request, 'StaffWorkspace/loginPage.html',context)
    else:
        if request.user.is_authenticated:            
            return redirect('../')
        else:
            return render(request, 'StaffWorkspace/loginPage.html')      

def logout_user(request):
    logout(request)
    return redirect('home')    

def home(request):
    """        General view for all user.    """
    if not request.user.is_authenticated:
        return redirect('login_user')
    else:
        return render(request, 'StaffWorkspace/home.html')


def input_form(request, catagory):
    """        Worker can input store related information.    """ 

    # As Catagory-id is foreign key it will just store it's pk to Item table that's 
    # why we need to search both Catagory and Item table to get proper dynamic filtering.
    catagory = Catagory.objects.get(name=catagory)          # Collecting the name of catagory
    items = Item.objects.filter(catagory=catagory.id)       # Filtering item name from items using catagory.id
    vendors = Vendor.objects.all()                          # Collecting all vendors
    stock_locations = StockLocation.objects.all()           # Collecting all stock locations

    # Sending all needed values to webpage via context
    context = {
        "form": WorkerInputForm,
        "items": items,
        "vendors": vendors,
        "stock_locations": stock_locations,
    }
    
    if not request.user.is_authenticated:
        return render(request, 'StaffWorkspace/loginPage.html')
    else:
        return render(request, 'StaffWorkspace/inputForm.html', context)


def input_form_submit(request):
    """ When form is submitted it will check and validate as wll as save data. """
    if request.method == "POST":                            # Checking the submit form request is post or not
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
        added_by = request.user.username                    # Getting the information of loged in user        
        # print(item_name, item_no, vendor, stock_location, cost_per_unit, previous_balance, issued, issued_to, ending_balance, comments)
        
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
        
        # Previous balance update depending on ending_balance. Table name = Item
        Item.objects.filter(name=item_name).update(balance=ending_balance)     
        
    
    if not request.user.is_authenticated:
        return render(request, 'StaffWorkspace/loginPage.html')
    else:
        return redirect('report')


def report(request):
    if not request.user.is_authenticated:
        return render(request, 'StaffWorkspace/loginPage.html')
    else:
        return render(request, "StaffWorkspace/report.html")

def report_daily(request, value=None):
    """        Report generation for worker.    """ 
    # Catching post values
    value1 = request.POST.get('date')  
    value2 = request.POST.get('month')  
    value3 = request.POST.get('itemNo')  
    value4 = request.POST.get('itemName')  
    value5 = request.POST.get('vendor')
    """   
    # Testing purpose
    print(value1)
    print(value2)
    print(value3)
    print(value4)
    print(datetime.now())
    """
    
    if value1 is not None:
        date = request.POST.get('date')
        report = Report.objects.filter(date = date)
    elif value2 is not None:
        month = request.POST.get('month')
        month, year = month.split("/")
        report = Report.objects.filter(date__year=year, date__month=month)
    elif value3 is not None:
        item_no = request.POST.get('itemNo')
        report = Report.objects.filter(item_no=item_no)
    elif value4 is not None:
        try:
            item_name = request.POST.get('itemName') 
            item_name = Item.objects.get(name =item_name) 
            report = Report.objects.filter(item_name=item_name.id)
        except:
            report = None
    elif value5 is not None:
        try:
            vendor = request.POST.get('vendor')
            vendor = Vendor.objects.get(name=vendor) 
            report = Report.objects.filter(vendor=vendor)
        except:
            report = None
    else:
        report = Report.objects.filter(date__year=datetime.now().year, date__month=datetime.now().month) # Only current months report
    
    # Sending all needed values to webpage via context
    context = {
        "date": datetime.now(),
        "report": report,
    }
    
    if not request.user.is_authenticated:
        return render(request, 'StaffWorkspace/loginPage.html')
    else:
        return render(request, 'StaffWorkspace/reportDaily.html', context)
    
    
def report_monthly(request, value=None):
    """     Monthly report generation item wise     """
    # Pre defined values default = 0
    purchase_item = 0
    issued_item = 0
    previous_balance = 0
    ending_balance = 0
    total_change = []                                                       # Trackng the change for individual changes
    value1 = request.POST.get('month')                                      # Getting the value from requester, method is POST
    report_item_in_this_month=set() 
    
    # If sender sends value of month then this comparison will start working
    if value1 is not None:
        month = request.POST.get('month')
        month, year = month.split("/")                                      # Dividing 10/2018 into month=10, year=2018
        item_all = Item.objects.all()                                       # All items
        reports = Report.objects.filter(date__year=year, date__month=month)  # Requesting for given month
        
        for r in reports:
            r_string = str(r.item_name)
            report_item_in_this_month.add(r_string) 
        print(report_item_in_this_month)
            
        for item_detail in item_all:                                              
            for report in reports:                
                if str(item_detail.name) == str(report.item_name):               # If there is any report on that month then continue  
                    previous_balance = Report.objects.filter(date__year=year, date__month=month, item_name=item_detail.id).first().previous_balance
                    purchase_item = purchase_item + report.purchase
                    issued_item = issued_item + report.issued
                    
            ending_balance = previous_balance + purchase_item - issued_item     # Ending balance calculation
                    
            if str(item_detail.name) not in report_item_in_this_month:          # Otherwise put last transition from any month
                report_not_in_this_month = Report.objects.filter(item_name=item_detail.id).last()
                try:                                                            # If there is any transition then continue        
                    previous_balance = report_not_in_this_month.ending_balance
                    ending_balance = report_not_in_this_month.ending_balance
                except:                                                         # Otherwise show except state
                    previous_balance = 0
                    ending_balance = 0
                    
            # All changes stored in total_change list to supply in template
            total_change.append([item_detail.item_no, item_detail.name, previous_balance, purchase_item, issued_item, ending_balance]) 
            """
            # Testing purpose
            print(item_detail.name, "=", total_change)
            print(item_detail.name, "=", purchase_item)
            print(item_detail.name, "=", issued_item)
            """
            # Reset default values
            purchase_item = 0
            issued_item = 0
            previous_balance = 0
            ending_balance = 0
    else:
        pass
        
    context = {
        "date": 'Monthly Report',
        "total_changes": total_change,
    }
    
    if not request.user.is_authenticated:
        return render(request, 'StaffWorkspace/loginPage.html')
    else:
        return render(request, 'StaffWorkspace/reportMonthly.html', context)
    
def buy_new_item(request):
    items = Item.objects.all()
    context={
        'items': items,
    }

    return render(request, 'StaffWorkspace/buyNewItem.html', context)