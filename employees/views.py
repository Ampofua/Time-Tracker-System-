# employees/views.py

from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Employee, TimeLog, Shift
import csv
from django.http import HttpResponse
from django.contrib import messages
from .models import Employee
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm


def register_employee(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Save the additional employee information
            Employee.objects.create(user=user, position=form.cleaned_data['position'])
            messages.success(request, 'Account created successfully. You can now log in.')
            return redirect('login')  # Redirect to login page after successful signup
    else:
        form = CustomUserCreationForm()

    return render(request, 'employees/register.html', {'form': form})





@login_required
def clock_in(request):
    employee = Employee.objects.get(user=request.user)
    if request.method == 'POST':
        # Ensure the employee isn't already clocked in
        if TimeLog.objects.filter(employee=employee, clock_out_time__isnull=True).exists():
            messages.error(request, "You are already clocked in.")
            return redirect('clock_in')
        TimeLog.objects.create(employee=employee, clock_in_time=timezone.now())
        messages.success(request, "Clocked in successfully.")
        return redirect('clock_out')
    return render(request, 'employees/clock_in.html')

@login_required
def clock_out(request):
    employee = Employee.objects.get(user=request.user)
    # Ensure the employee has clocked in but not clocked out yet
    time_log = TimeLog.objects.filter(employee=employee, clock_out_time__isnull=True).first()
    
    if not time_log:
        messages.error(request, "You have not clocked in yet.")
        return redirect('clock_in')

    if request.method == 'POST':
        time_log.clock_out_time = timezone.now()
        time_log.save()
        messages.success(request, "Clocked out successfully.")
        return redirect('clock_in')
    return render(request, 'employees/clock_out.html')

@login_required
def admin_dashboard(request):
    employees = Employee.objects.all()
    time_logs = TimeLog.objects.all()
    return render(request, 'employees/admin_dashboard.html', {'employees': employees, 'time_logs': time_logs})


def profile_view(request):
    employee = Employee.objects.get(user=request.user)
    return render(request, 'employees/profile.html', {'employee': employee})


def profile(request):
    user = request.user
    try:
        employee = Employee.objects.get(user=user)
    except Employee.DoesNotExist:
        employee = None  # Handle cases where the employee record doesn't exist

    context = {
        'user': user,
        'employee': employee,
    }
    return render(request, 'profile.html', context)



@login_required
def export_timesheets_csv(request):
    time_logs = TimeLog.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="timesheets.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Employee', 'Clock In', 'Clock Out', 'Hours Worked'])
    
    for log in time_logs:
        # Ensure that both clock in and clock out times are present
        if log.clock_out_time:
            hours_worked = (log.clock_out_time - log.clock_in_time).total_seconds() / 3600
        else:
            hours_worked = "N/A"  # Clock out not completed

        writer.writerow([log.employee.user.username, log.clock_in_time, log.clock_out_time or "N/A", hours_worked])
    
    return response

