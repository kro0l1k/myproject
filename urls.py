from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
    
    # Include forum URLs with a namespace
    path('forum/', include(('forum.urls', 'forum'), namespace='forum')),
]
