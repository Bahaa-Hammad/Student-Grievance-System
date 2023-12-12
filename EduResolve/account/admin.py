from django.utils.html import format_html
from django.urls import reverse
from urllib.parse import urlencode
from grievance.models import Grievance
from .models import Account, Department
from django.contrib import admin
from django.contrib.auth.models import Group

admin.site.site_header = 'EduResolve'
admin.site.site_title = 'EduResolve'
admin.site.index_title = 'EduResolve'


class AccountAdmin(admin.ModelAdmin):
    def add_to_grievance_staff(modeladmin, request, queryset):
        group_name = "grievance_staff"
        group = Group.objects.get(name=group_name)
        for account in queryset:
            account.groups.add(group)
                
    def total_grievances(self, obj):
        return Grievance.objects.filter(student=obj).count()
        
    total_grievances.short_description = 'Total Grievances Submitted'
    
    def view_grievances(self, obj):
            count = self.total_grievances(obj)
            if count > 0:
                try:
                    url = reverse("admin:grievance_grievance_changelist")
                    url_with_query = url + "?" + urlencode({"student__id": f"{obj.id}"})
                    return format_html('<a href="{}">View {} Grievances</a>', url_with_query, count)
                except Exception as e:
                    print("Error in reverse function:", e)
                    return "Error generating URL"
            return "No Grievances"

    view_grievances.short_description = 'Grievances'

    list_display = ['email', 'first_name', 'last_name', 'total_grievances', 'view_grievances'] 
    ordering = ['email']
    actions = [add_to_grievance_staff, total_grievances]
    search_fields = ['email']

admin.site.register(Account, AccountAdmin)
admin.site.register(Department)
