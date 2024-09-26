from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views

def home_redirect(request):
    return redirect('clock_in')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('employees/', include('employees.urls')),
    path('', home_redirect),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login')
    
]

