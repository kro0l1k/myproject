from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Home page
    path('', views.home, name='home'),
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    # Tutorials
    path('tutorials/', views.tutorials, name='tutorials'),
    # Challenges
    path('challenges/', views.challenges, name='challenges'),
    # ... other URLs ...
] 