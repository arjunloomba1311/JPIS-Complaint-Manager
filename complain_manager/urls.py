
from django.contrib import admin
from django.urls import path, include

from django.conf import settings # importing the settings.py file
from django.conf.urls.static import static


import complaints.views
import accounts.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',complaints.views.home,name = 'home'),
    path('accounts/',include('accounts.urls')),
    path('complaints/',include('complaints.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
