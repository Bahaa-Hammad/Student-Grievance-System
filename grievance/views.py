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
            grievance = form.save(commit=False)
            grievance.student = student
            grievance.save()
            print(grievance)
            return redirect('grievances')

    context = {'form': form}
    return render(request, "grievance/grievance-submission.html", context)


@login_required(login_url="login")
def submited_grievances(request):
    student = request.user
    grievances = Grievance.objects.get(student=student)
    return render(request, 'grievance/submited_grievances.html', {'grievances': grievances})


@login_required(login_url="login")
def grievance(request, pk):
    student = request.user

    grievance = Grievance.objects.get(student=student, id=pk)
    return render(request, 'grievance/grievance.html', {'grievance': grievance})
