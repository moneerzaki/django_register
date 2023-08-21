from django.shortcuts import render, redirect
from django.forms import modelformset_factory
from .models import Student
from .models import AttendanceRecord
from django.contrib.auth.decorators import login_required
from .forms import StudentForm
from django.contrib import messages
from django.forms.utils import ErrorList
# from django.db.models import Q
from datetime import date

# those ones for user_username authentication
from functools import wraps
from django.shortcuts import HttpResponse
def specific_username_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Get the authenticated user
        user = request.user

        # Check if the user's username is the desired one
        if user.username == 'khadem':
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("You are not authorized to access this view.")
    return login_required(_wrapped_view)


# Create your views here.

@specific_username_required
def edit_student(request, student_id):
    student = Student.objects.get(id=student_id)
    studentForm = StudentForm(request.POST or None, instance=student)
    if request.method == 'POST':
        if studentForm.is_valid():
            student = studentForm.save()
        return redirect('project2:info')  # Redirect to the desired URL
    return render(request, "project2/edit_student.html", {"student": student, "studentForm": studentForm})


@specific_username_required
def ebtda2y(request):
    return render(request, "project2/ebtda2y.html", {})


@specific_username_required
def info(request): 
    context = {
            'students': Student.objects.all(),
            # 'guardians': Guardian.objects.all()
        }
    
    return render(request, "project2/info.html", context)
    # return render(request, "register/homepage.html", {})


#with guardian info inside student class
@specific_username_required
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


@specific_username_required
def birthdays (request):
    current_month = date.today().month
    target_months = [current_month, (current_month + 1) % 12, (current_month + 2) % 12]
    matching_students = Student.objects.filter(Q(date_of_birth__month__in=target_months))
    return render(request, "project2/birthdays.html", {'matching_students':matching_students})


# @specific_username_required
# def attendance (request):

#     return render(request, "project2/attendance_general.html", {})

@specific_username_required
def attendance(request):
    dates = AttendanceRecord.objects.order_by('date').values_list('date', flat=True).distinct()
    students = Student.objects.all()
    attendance_records = AttendanceRecord.objects.all()

    attendance_data = []
    for student in students:
        student_data = {
            'name': student.name,
            'academic_year': student.academic_year,
            'attendance_status': []
        }
        for date in dates:
            student_names_attended = attendance_records.filter(date=date).values_list('students_present', flat=True)
            if any(student.name in names.split(',') for names in student_names_attended):
                attendance_status="attended"
                print("*****************attended******************")
            else:
                attendance_status=""
                print("*****************did not attend******************")
            # attendance_status = 'attended' if attendance_records.filter(students_present=student, date=date).exists() else ''
            student_data['attendance_status'].append(attendance_status)
        attendance_data.append(student_data)
    
    print("here ------------------ here ")
    print(dates)
    print("here ------------------ here ")
    # print(students[2])
    # print(attendance_records.filter(students_present=student, date=dates.first()).exists())
    print(attendance_data[2])

    context = {
        'dates': dates,
        'attendance_data': attendance_data,
    }

    return render(request, 'project2/attendance_general.html', context)



@specific_username_required
def attendance_12(request):
    if request.method == 'POST':
        attended_names = request.POST.getlist('attended_names')
        day_title = "مدارس احد"  # Set the day title as needed
        attendance_record = AttendanceRecord(day_title=day_title)
        attendance_record.save()

        for name in attended_names:
            student = Student.objects.get(name=name)
            attendance_record.mark_attendance(student)
        
        attendance_record.save()

    students_1= Student.objects.filter(academic_year=1)
    # print("number of students in class 1: ",len(students_1))
    students_2= Student.objects.filter(academic_year=2)
    # print("number of students in class 2:",len(students_2))
    context = {'students_1': students_1, 'students_2': students_2 }
    return render(request, "project2/attendance_12.html", context)


@specific_username_required
def attendance_34 (request):
    
    return render(request, "project2/attendance_34.html", {})


@specific_username_required
def attendance_56 (request):
    
    return render(request, "project2/attendance_56.html", {})
