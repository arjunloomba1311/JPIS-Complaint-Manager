from django.contrib import admin

from .models import complaint_info, admin_complaints
# Register your models here.
admin.site.register(complaint_info)
admin.site.register(admin_complaints)
