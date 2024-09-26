# employees/urls.py

from django.urls import path
from . import views
from .views import register_employee
# from .views import CustomPasswordChangeView

urlpatterns = [
    path('clock-in/', views.clock_in, name='clock_in'),
    path('clock-out/', views.clock_out, name='clock_out'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('export-timesheets/', views.export_timesheets_csv, name='export_timesheets'),
    path('profile/', views.profile_view, name='profile'),
    path('register/', register_employee, name='register_employee')
    

]
