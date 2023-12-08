from django.contrib import admin
from .models import Grievance, GrievanceNotification
from django.contrib import messages
from apis.postmark.handler import send_notification_email 


from django import forms

class GrievanceAdminForm(forms.ModelForm):
    admin_message = forms.CharField(widget=forms.Textarea, required=False, label="Admin Message")

    class Meta:
        model = Grievance
        fields = '__all__'
        

from django.contrib import admin
from .models import Grievance, GrievanceNotification

@admin.register(Grievance)
class GrievanceAdmin(admin.ModelAdmin):
    form = GrievanceAdminForm
    list_display = ['subject', 'student', 'status']
    ordering = ['date']

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
            
admin.site.register(GrievanceNotification)
