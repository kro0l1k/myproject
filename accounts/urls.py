from django.urls import path
from . import views

urlpatterns = [
    # Home page view
    path('', views.home, name='home'),
    # Registration page
    path('register/', views.register, name='register'),
    path('tutorials/', views.tutorials, name='tutorials'),
    path('challenge/', views.challenge, name='challenge'),
    path('community/', views.community, name='community'),
    path('signup/', views.register, name='signup'),  # Alias for registration
]
