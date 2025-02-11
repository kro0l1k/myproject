from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Home page
    path('', views.home, name='home'),
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    # ... other URLs ...
] 