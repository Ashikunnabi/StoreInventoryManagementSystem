from datetime import datetime
from django.shortcuts import render
from .forms import WorkerInputForm

def home(request):
    """        General view for all user.    """
    return render(request, 'StaffWorkspace/home.html')
    
def input_form(request):
    """        Worker can input store related information.    """
    context={
        "form": WorkerInputForm
    }
    return render(request, 'StaffWorkspace/inputForm.html', context)
    
def worker_report(request):
    """        Report generation for worker.    """
    context={
        "date": datetime.now()
    }
    return render(request, 'StaffWorkspace/workerReport.html', context)
    
def worker_report_print(request):
    """        Report print for worker.    """
    return render(request, 'StaffWorkspace/workerReportPrint.html')
