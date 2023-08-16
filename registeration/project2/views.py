from django.shortcuts import render, redirect
from django.forms import modelformset_factory
from .models import Student
# from .models import Guardian
from django.contrib.auth.decorators import login_required
from .forms import StudentForm
from django.contrib import messages
from django.forms.utils import ErrorList


# Create your views here.

@login_required
def edit_student(request, student_id):
    student = Student.objects.get(id=student_id)
    studentForm = StudentForm(request.POST or None, instance=student)
    if request.method == 'POST':
        if studentForm.is_valid():
            student = studentForm.save()
        return redirect('project2:info')  # Redirect to the desired URL
    return render(request, "project2/edit_student.html", {"student": student, "studentForm": studentForm})


@login_required
def ebtda2y(request):
    return render(request, "project2/ebtda2y.html", {})


@login_required
def info(request): 
    context = {
            'students': Student.objects.all(),
            # 'guardians': Guardian.objects.all()
        }
    
    return render(request, "project2/info.html", context)
    # return render(request, "register/homepage.html", {})


#with guardian info inside student class
@login_required
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)

        # Checking the validity of the entered name. 
        student_name = request.POST.get("name")
        student_name_parts = student_name.split()
        students = Student.objects.filter(name=student_name)
        if len(student_name_parts) < 2:
            form.add_error("name", "Please enter the full name of the student at least till father name.")
        elif students: 
            form.add_error("name", "this name has already been entered once")

        elif form.is_valid():
            student = form.save()
            messages.success(request, f"Student {student_name} added successfully!")
            # return redirect('success_page')  # Redirect to a success page if needed
    else:
        form = StudentForm()
    return render(request, 'project2/add_student.html', {'form': form})


