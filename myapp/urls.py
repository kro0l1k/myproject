from django.urls import path
from . import views

app_name = 'myapp'

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    # ... other URLs ...
] 