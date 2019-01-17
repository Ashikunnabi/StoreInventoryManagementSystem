from django.contrib.auth import authenticate, login, logout
import calendar
from datetime import datetime, date
from django.shortcuts import render, redirect
from .forms import WorkerInputForm
from .models import Report

from AdminWorkspace.models import Catagory, Item, StockLocation, Vendor


def login_user(request):
    """     Login      """
    if request.method == "POST":                        # If method=POST then request is valid otherwise not
        username = request.POST['username']             # Collecting username
        password = request.POST['password']             # Collecting password
        user = authenticate(username=username, password=password) # If user is valid then authenticte otherwise not
        if user is not None:
            login(request, user)                        # If valid user then login
            return redirect('home')
        else:                                           # If username / password is wrong
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
    """     Logout      """
    logout(request)                                 # Logout - all session and permission will be invalid
    return redirect('login_user')


def home(request):
    """        General view for all user.    """
    catagory = Catagory.objects.all()
    context = {
        "catagories": catagory
    }
    if not request.user.is_authenticated:
        return redirect('login_user')
    else:
        return render(request, 'StaffWorkspace/home.html', context)


def input_form(request, catagory):
    """        Worker can input store related information.    """
    _catagory = catagory                                    # Passing catagory to template
    # As Catagory-id is foreign key it will just store it's pk to Item table that's
    # why we need to search both Catagory and Item table to get proper dynamic filtering.
    catagory = Catagory.objects.get(name=catagory)          # Collecting the name of catagory
    items = Item.objects.filter(catagory=catagory.id).order_by('name')       # Filtering item name from items using catagory.id
    vendors = Vendor.objects.all()                          # Collecting all vendors
    stock_locations = StockLocation.objects.all().order_by('name')           # Collecting all stock locations

    # Sending all needed values to webpage via context
    context = {
        "form": WorkerInputForm,
        "items": items,
        "vendors": vendors,
        "stock_locations": stock_locations,
        "catagory": _catagory,
    }

    if not request.user.is_authenticated:
        return render(request, 'StaffWorkspace/loginPage.html')
    else:
        return render(request, 'StaffWorkspace/inputForm.html', context)


def input_form_submit(request, catagory):
    """ When form is submitted it will check and validate as wll as save data. """
    if request.method == "POST":                            # Checking the submit form request is post or not
        # If your request is post then only this conditon will run otherwise not.
        item_name = request.POST.get("item_name")
        vendor = request.POST.get("vendor_name")
        stock_location = request.POST.get("stock_location")
        cost_per_unit = request.POST.get("cost_per_unit")
        previous_balance = request.POST.get("previous_balance")
        purchase = request.POST.get("purchase")
        issued = request.POST.get("issued")
        ending_balance = request.POST.get("ending_balance")
        issued_to = request.POST.get("issued_to")
        comments = request.POST.get("comments")
        added_by = request.user.username                    # Getting the information of loged in user
        # print(item_name, item_no, vendor, stock_location, cost_per_unit, previous_balance, issued, issued_to, ending_balance, comments)

        if purchase == '0' and issued == '0':               # If javascript is not available then this one will arise
            error = "Something went wrong. Please reset your browser or enable javascript."
            context = {
                "error": error,
                "catagory": catagory,
                "noJavaScript": "disabled",
            }
            return render(request, 'StaffWorkspace/inputForm.html', context)
        else:
            # Collecting the information of a row/object from diffrent model/table.
            item_detail = Item.objects.get(name=item_name)
            catagory_detail = Catagory.objects.get(name=item_detail.catagory)
            vendor_detail = Vendor.objects.get(name=vendor)
            stock_detail = StockLocation.objects.get(name=stock_location)

            try:    # If valid data inputed
                    # Making a query to Report table to save data.
                report_save = Report( item_name = Item.objects.get(pk=item_detail.id),
                            item_no = item_detail.item_no,
                            catagory = Catagory.objects.get(pk=catagory_detail.id),
                            vendor=Vendor.objects.get(pk=vendor_detail.id),
                            stock_location=StockLocation.objects.get(pk=stock_detail.id),
                            cost_per_unit = cost_per_unit,
                            previous_balance=int(previous_balance),
                            purchase =  purchase,
                            issued =issued,
                            ending_balance = ending_balance,
                            issued_to = issued_to,
                            comments = comments,
                            added_by = added_by)
                report_save.save()
                # Previous balance update depending on ending_balance. Table name = Item
                Item.objects.filter(name=item_name).update(balance=ending_balance, cost_per_unit=cost_per_unit)

            except:     # Invalid data inputed
                error = "Something went wrong. Please reset your browser or enable javascript."
                context = {
                    "error": error,
                    "catagory": catagory,
                    "noJavaScript": "disabled",
                }
                return render(request, 'StaffWorkspace/inputForm.html', context)

    if not request.user.is_authenticated:
        return render(request, 'StaffWorkspace/loginPage.html')
    else:
        return redirect('input_form', catagory=catagory_detail.name)


def report(request, catagory=None):
    """     Report page of wathing diffrent types of report     """
    if not request.user.is_authenticated:
        return render(request, 'StaffWorkspace/loginPage.html')
    else:
        return render(request, "StaffWorkspace/report.html", {'catagory':catagory})


def report_daily(request, catagory=None, value=None):
    """        Report generation for worker.    """
    # Catching post values
    value1 = request.POST.get('date')
    value2 = request.POST.get('month')
    value3 = request.POST.get('itemNo')
    value4 = request.POST.get('itemName')
    value5 = request.POST.get('vendor')

    # If no catagory is selected
    if catagory == 'None':
        # If user request for specific type of data to see report
        if value1 is not None:
            date = request.POST.get('date')
            report = Report.objects.filter(date = date)
        elif value2 is not None:
            month = request.POST.get('month')
            month, year = month.split("/")
            report = Report.objects.filter(date__year=year, date__month=month)
        elif value3 is not None:
            try:
                item_no = request.POST.get('itemNo')
                report = Report.objects.filter(item_no=item_no).order_by('-date')[:500]
            except:
                report = None
        elif value4 is not None:
            try:
                item_name = request.POST.get('itemName')
                item_name = Item.objects.get(name =item_name)
                report = Report.objects.filter(item_name=item_name.id).order_by('-date')[:500]
            except:
                report = None
        elif value5 is not None:
            try:
                vendor = request.POST.get('vendor')
                vendor = Vendor.objects.get(name=vendor)
                report = Report.objects.filter(vendor=vendor)
            except:
                report = None
        else:                                                                # Otherwise default data will be shown
            report = Report.objects.filter(date__year=datetime.now().year,
                                   date__month=datetime.now().month) # Only current months report
        report_search_suggest = Item.objects.all()                   # Auto suggest field for search option

    else:           # If catagory is selected
        catagory = Catagory.objects.get(name=catagory)
        # If user request for specific type of data to see report
        if value1 is not None:
            date = request.POST.get('date')
            report = Report.objects.filter(date = date, catagory = catagory.id)
        elif value2 is not None:
            month = request.POST.get('month')
            month, year = month.split("/")
            report = Report.objects.filter(date__year=year, date__month=month, catagory = catagory.id)
        elif value3 is not None:
            try:
                item_no = request.POST.get('itemNo')
                report = Report.objects.filter(item_no=item_no, catagory = catagory.id).order_by('-date')[:50]
            except:
                report = None
        elif value4 is not None:
            try:
                item_name = request.POST.get('itemName')
                item_name = Item.objects.get(name =item_name)
                report = Report.objects.filter(item_name=item_name.id, catagory = catagory.id).order_by('-date')[:50]
            except:
                report = None
        elif value5 is not None:
            try:
                vendor = request.POST.get('vendor')
                vendor = Vendor.objects.get(name=vendor)
                report = Report.objects.filter(vendor=vendor, catagory = catagory.id)
            except:
                report = None
        else:                                                                # Otherwise default data will be shown
            report = Report.objects.filter(date__year=datetime.now().year,
                                        date__month=datetime.now().month, catagory = catagory.id) # Only current months report
        report_search_suggest = Item.objects.filter(catagory = catagory.id)     # Auto suggest field for search option

    # Sending all needed values to webpage via context
    context = {
        "date": datetime.now(),
        "report": report,
        "report_search_suggest": report_search_suggest,
        "catagory": catagory,
    }

    if not request.user.is_authenticated:
        return render(request, 'StaffWorkspace/loginPage.html')
    else:
        return render(request, 'StaffWorkspace/reportDaily.html', context)


def report_monthly(request, catagory=None, value=None):
    """     Monthly report generation item wise     """
    # Pre defined values default = 0
    purchase_item = 0
    issued_item = 0
    previous_balance = 0
    ending_balance = 0
    total_purchase_cost = 0
    total_change = []                                                       # Trackng the change for individual changes
    value1 = request.POST.get('month')                                      # Getting the value from requester, method is POST
    report_item_in_this_month=set()

    # If sender sends value of month then this comparison will start working
    if catagory == 'None':
        if value1 is not None:
            month = request.POST.get('month')
            month, year = month.split("/")                                       # Dividing 10/2018 into month=10, year=2018
            item_all = Item.objects.all()                                        # All items
            reports = Report.objects.filter(date__year=year, date__month=month)  # Requesting for given month

            # Making a set of reported item list of searched month
            for r in reports:
                r_string = str(r.item_name)
                report_item_in_this_month.add(r_string)

            for item_detail in item_all:                                            # All items
                for report in reports:                                              # Reort of searched month
                    if str(item_detail.name) == str(report.item_name):              # If there is any report on that month then continue
                        previous_balance = Report.objects.filter(date__year=year, date__month=month, item_name=item_detail.id).first().previous_balance
                        purchase_item = purchase_item + report.purchase
                        issued_item = issued_item + report.issued
                        total_purchase_cost = total_purchase_cost + (report.cost_per_unit * report.purchase)

                ending_balance = previous_balance + purchase_item - issued_item     # Ending balance calculation

                if str(item_detail.name) not in report_item_in_this_month:          # Otherwise put last transition from last month
                    if int(month) == 1:
                        days_in_month = calendar.monthrange(int(year)-1, 12)[1] # Getting how many days in one month
                        report_not_in_this_month = Report.objects.filter(date__range=[datetime(2000,1,1), datetime(int(year)-1, 12, days_in_month)],
                                                                        item_name=item_detail.id).last()
                    else:
                        days_in_month = calendar.monthrange(int(year), int(month)-1)[1] # Getting how many days in one month
                        report_not_in_this_month = Report.objects.filter(date__range=[datetime(2000,1,1), datetime(int(year), int(month)-1, days_in_month)],
                                                                        item_name=item_detail.id).last()
                    try:                                                            # If there is any transition then continue
                        previous_balance = report_not_in_this_month.ending_balance
                        ending_balance = report_not_in_this_month.ending_balance
                        total_purchase_cost = 0
                    except:                                                         # Otherwise show except state
                        previous_balance = item_detail.balance
                        ending_balance = item_detail.balance
                        total_purchase_cost = 0

                # All changes stored in total_change list to supply in template
                total_change.append([item_detail.item_no, item_detail.name, previous_balance, purchase_item, issued_item, ending_balance, total_purchase_cost])
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
                total_purchase_cost = 0
            report_search_suggest = Item.objects.all()          # Auto suggest field for search option
        else:
            report_search_suggest = None

    else:
        catagory = Catagory.objects.get(name=catagory)
        if value1 is not None:
            month = request.POST.get('month')
            month, year = month.split("/")                                      # Dividing 10/2018 into month=10, year=2018
            item_all = Item.objects.filter(catagory = catagory.id)                                       # All items
            reports = Report.objects.filter(date__year=year, date__month=month, catagory = catagory.id)  # Requesting for given month

            # Making a set of reported item list of searched month
            for r in reports:
                r_string = str(r.item_name)
                report_item_in_this_month.add(r_string)

            for item_detail in item_all:                                            # All items
                for report in reports:                                              # Reort of searched month
                    if str(item_detail.name) == str(report.item_name):              # If there is any report on that month then continue
                        previous_balance = Report.objects.filter(date__year=year, date__month=month, item_name=item_detail.id).first().previous_balance
                        purchase_item = purchase_item + report.purchase
                        issued_item = issued_item + report.issued
                        total_purchase_cost = total_purchase_cost + (report.cost_per_unit * report.purchase)

                ending_balance = previous_balance + purchase_item - issued_item     # Ending balance calculation

                if str(item_detail.name) not in report_item_in_this_month:          # Otherwise put last transition from last month                                                          
                    if int(month) == 1:
                        days_in_month = calendar.monthrange(int(year)-1, 12)[1] # Getting how many days in one month
                        report_not_in_this_month = Report.objects.filter(date__range=[datetime(2000,1,1), datetime(int(year)-1, 12, days_in_month)],
                                                                        item_name=item_detail.id).last()
                    else:
                        days_in_month = calendar.monthrange(int(year), int(month)-1)[1] # Getting how many days in one month
                        report_not_in_this_month = Report.objects.filter(date__range=[datetime(2000,1,1), datetime(int(year), int(month)-1, days_in_month)],
                                                                        item_name=item_detail.id).last()                                                    
                    try:                                                            # If there is any transition then continue
                        previous_balance = report_not_in_this_month.ending_balance
                        ending_balance = report_not_in_this_month.ending_balance
                        total_purchase_cost = 0
                    except:                                                         # Otherwise show except state
                        previous_balance = item_detail.balance
                        ending_balance = item_detail.balance
                        total_purchase_cost = 0

                # All changes stored in total_change list to supply in template
                total_change.append([item_detail.item_no, item_detail.name, previous_balance, purchase_item, issued_item, ending_balance, total_purchase_cost])
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
                total_purchase_cost = 0
            report_search_suggest = Item.objects.filter(catagory = catagory.id)                 # Auto suggest field for search option
        else:
            report_search_suggest = None

    context = {
        "date": value1,
        "total_changes": total_change,
        "report_search_suggest": report_search_suggest,
        "catagory": catagory,
    }

    if not request.user.is_authenticated:
        return render(request, 'StaffWorkspace/loginPage.html')
    else:
        return render(request, 'StaffWorkspace/reportMonthly.html', context)


def buy_new_item(request):
    """     If any item needs to buy it will generate that item list    """
    items = Item.objects.all()
    context={
        'items': items,
    }

    if not request.user.is_authenticated:
        return render(request, 'StaffWorkspace/loginPage.html')
    else:
        return render(request, 'StaffWorkspace/buyNewItem.html', context)


def graph(request):
    """     If any item needs to buy it will generate that item list    """
    items_balance = Item.objects.all()
    reports = Report.objects.filter(date__year=datetime.now().year, date__month=datetime.now().month) # Only current months report
    context={
        'items_balance': items_balance,
        'reports': reports,
    }

    if not request.user.is_authenticated:
        return render(request, 'StaffWorkspace/loginPage.html')
    else:
        return render(request, 'StaffWorkspace/graph.html', context)