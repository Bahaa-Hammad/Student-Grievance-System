from django.contrib import admin
from .models import Account, Department
from django.contrib import admin
    
admin.site.site_header = 'Student Grievance System'
admin.site.site_title = 'Student Grievance System'
admin.site.index_title = 'Student Grievance System'

admin.site.register(Account)
admin.site.register(Department)
