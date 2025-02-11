"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Include Django's built-in authentication URLs:
    path('accounts/', include('django.contrib.auth.urls')),
    # Include our custom accounts app URLs:
    path('accounts/', include('accounts.urls')),
    # For simplicity, let's define a home page:
    path('', include('accounts.urls')),  # home page will be defined in accounts.urls
    # Include forum URLs with namespace:
    path('forum/', include(('forum.urls', 'forum'), namespace='forum')),
]
