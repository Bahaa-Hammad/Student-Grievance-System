from django.contrib import admin
from .models import Grievance, GrievanceNotification
from django.contrib import messages
from apis.postmark.handler import send_notification_email 
from django import forms
from django.utils.html import format_html

class GrievanceAdminForm(forms.ModelForm):
    admin_message = forms.CharField(widget=forms.Textarea, required=False, label="Admin Message")

    class Meta:
        model = Grievance
        fields = '__all__'

@admin.register(Grievance)
class GrievanceAdmin(admin.ModelAdmin):
    form = GrievanceAdminForm
            
    def get_queryset(self, request):
            qs = super().get_queryset(request)
            if request.user.is_superuser:
                return qs  # Superuser can see all grievances
            if request.user.is_staff:
                return qs.filter(department=request.user.department)
            return qs.none()  # Non-staff users can't see any grievances
    
    def viewed_status(self, obj):
        return format_html('<b>{}</b>', 'Viewed' if obj.viewed_by_admin else 'Never Viewed')
    
    viewed_status.short_description = 'Viewed Status'
    
    def save_model(self, request, obj, form, change):
        # Check if the status has changed
        if 'status' in form.changed_data:
            # Save the grievance to capture the status change
            super().save_model(request, obj, form, change)

            # Get the student's email who submitted the grievance
            student_email = obj.student.email if obj.student and obj.student.email else "No email"
            note = form.cleaned_data.get('admin_message', 'Status changed.')
            # Send a notification
            notification = GrievanceNotification.objects.create(
                grievance=obj,
                message=f"Status changed to {obj.get_status_display()}. {note}"
            )
            send_notification_email(request,student_email,notification.message)
        else:
            super().save_model(request, obj, form, change)    
    list_display = ['id','subject', 'student', 'status']
    ordering = ['date']
    search_fields = ['id', 'subject', 'student__email']
    list_filter = ['status']
            
admin.site.register(GrievanceNotification)
