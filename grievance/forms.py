from django import forms
from .models import Grievance, Department


class GrievanceForm(forms.Form):
    subject = forms.CharField()
    type_of_complaint = forms.MultipleChoiceField(choices=Grievance.TYPE)
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=False)
    description = forms.CharField()
    subject.widget.attrs.update({'class': 'form-control form-control-lg'})
    type_of_complaint.widget.attrs.update({'class': 'form-control form-control-lg'})
    description.widget.attrs.update({'class': 'form-control form-control-lg'})
    department.widget.attrs.update({'class': 'form-control form-control-lg'})

    class Meta:
        model = Grievance
