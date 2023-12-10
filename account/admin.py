from django.contrib import admin
from .models import Account, Department
from django.contrib import admin
    
admin.site.site_header = 'EduResolve'
admin.site.site_title = 'EduResolve'
admin.site.index_title = 'EduResolve'

admin.site.register(Account)
admin.site.register(Department)
