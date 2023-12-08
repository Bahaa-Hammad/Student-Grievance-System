from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import GrievanceForm
from django.contrib.auth.decorators import login_required
from .models import Department, Grievance


@login_required(login_url="login")
def submit_grievance(request):

    student = request.user
    form = GrievanceForm()
    
    if request.method == 'POST':
        form = GrievanceForm(request.POST)
        if form.is_valid():
            subject=form.cleaned_data.get('subject')
            type_of_complaint=form.cleaned_data.get('type_of_complaint')
            department=form.cleaned_data.get('department')
            description=form.cleaned_data.get('description')
            student=request.user

            grievance = Grievance.create_student_grievance(subject=subject, type_of_complaint=type_of_complaint,department=department,description=description,student=student)
            if grievance:
                return redirect('dashboard')
            else:
                messages.error(request, 'An error has occurred during registration')


    context = {'form': form}
    return render(request, "grievance/grievance-submission.html", context)


@login_required(login_url="login")
def submited_grievances(request):
    student = request.user
    grievances = Grievance.get_student_grievances(student)
    return render(request, 'grievance/submited_grievances.html', {'grievances': grievances})


@login_required(login_url="login")
def grievance(request, pk):
    student = request.user

    grievance = Grievance.get_student_grievance(id=pk, student=student)
    return render(request, 'grievance/grievance.html', {'grievance': grievance})
