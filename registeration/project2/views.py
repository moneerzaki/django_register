from django.shortcuts import render, redirect
from django.forms import modelformset_factory
from .models import Student
from .models import AttendanceRecord
from django.contrib.auth.decorators import login_required
from .forms import StudentForm
from .forms import AttendanceRecordForm
from django.contrib import messages
from django.forms.utils import ErrorList
from django.db.models import Q, F   
from datetime import date
# those ones for user_username authentication
from functools import wraps
from django.shortcuts import HttpResponse
from .utils import *


# general functions 

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
    return _wrapped_view  # Remove login_required here



# Create your views here.

@specific_username_required
def edit_student(request, student_id):
    student = Student.objects.get(id=student_id)
    studentForm = StudentForm(request.POST or None, instance=student)
    if request.method == 'POST':
        # Checking the validity of the entered name. and other info 
        student_name = request.POST.get("name")
        students = Student.objects.filter(name=student_name)
        if student_name: 
            student_name_parts = student_name.split()
            if len(student_name_parts) < 2:
                studentForm.add_error("name", "Please enter the full name of the student at least till father name.")
        elif students: 
            studentForm.add_error("name", "this name has already been entered once")
        if studentForm.is_valid():
            studentForm.save()
            print(" edits have been saved ")
            messages.success(request, 'Edits have been saved successfully.')
            return redirect('project2:info')  # Redirect to the desired URL
        
        else: 
            print(studentForm.errors)  # Print form errors to the console for debugging
            messages.error(request, "something went wrong")
    return render(request, "project2/edit_student.html", {"student": student, "studentForm": studentForm})


@specific_username_required
def ebtda2y(request):
    calculate_absences()
    return render(request, "project2/ebtda2y.html", {})


@specific_username_required
def info(request): 
    context = {
            'students': Student.objects.all(),
            # 'guardians': Guardian.objects.all()
        }
    
    return render(request, "project2/info.html", context)
    # return render(request, "register/homepage.html", {})



@login_required
@specific_username_required  # Apply specific_username_required after login_required
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        print(request.POST)
        if form.is_valid():
            # Checking the validity of the entered name. and other info 
            # student_name = request.POST.get("name")
            # student_name = form.cleaned_data.get("name")
            student_name = form.cleaned_data.get('name')
            student_name_parts = student_name.split()
            students = Student.objects.filter(name=student_name)
            print("name length:  ----------->>>", student_name)
            print("data type:    ----------->>>", type(student_name))
            print("student name: ----------->>>", len(student_name_parts))

            if len(student_name_parts) < 2:
                form.add_error("name", "Please enter the full name of the student at least till father name.")
                print("name length is not enough")
            elif students: 
                form.add_error("name", "this name has already been entered once")
                print(" the name has been entered once before")
            elif form.is_valid():
                form.save()
                messages.success(request, f"Student {student_name} added successfully!")
                return redirect('project2:info')  # Redirect to the desired URL
                # return redirect('success_page')  # Redirect to a success page if needed
        else: 
            messages.error(request, f"form is invalid for some reason")
            print("form is invalid for somereason")
    else:
        form = StudentForm()
        
    return render(request, 'project2/add_student.html', {'form': form})


@specific_username_required
def birthdays (request):
    current_month = date.today().month
    target_months = [current_month, (current_month + 1) % 12, (current_month + 2) % 12]
    matching_students = Student.objects.filter(Q(date_of_birth__month__in=target_months) & Q(academic_year__range=(-2,2)))

    # Convert date_of_birth to sortable format
    for student in matching_students:
        student.date_of_birth_sortable = student.date_of_birth.strftime("%m-%d")
    return render(request, "project2/birthdays.html", {'matching_students':matching_students})


# @specific_username_required
# def attendance (request):

#     return render(request, "project2/attendance_general.html", {})


@specific_username_required
def attendance_general(request):

    objects = AttendanceRecord.objects.all()
    for object in objects: 
        object.save()

    calculate_absences()

    dates = AttendanceRecord.objects.filter(academic_year='12').order_by('date')
    # print ("view. attendance_general number of dates: " , len(dates))

    students = Student.objects.filter(academic_year__range=(-2, 2))
    # students = Student.objects.all()

    # attendance_records = AttendanceRecord.objects.all()

    attendance_data = []
    for student in students:
        counter=0
        student_data = {
            'name': student.name,
            'academic_year': student.academic_year,
            'absences': student.absences,
            'attendance_rate': student.attendance_rate,
            'attendance_status': []
        }
        for date in dates:
            if dates:
                student_names_attended = date.students_present.split(",")

                if student.name in student_names_attended:
                    attendance_status="attended"
                    if date.day_title == "مدارس احد":
                        counter += 1
                        if counter == 4:
                            attendance_status="4_weeks_bonus"
                            counter = 0
                        # print( date.date, " -- ",  student.name, "*****************",attendance_status,"******************", counter)
                    # else:
                    #     counter = 0
                else: 
                    attendance_status=""
                    if date.day_title == "مدارس احد":
                        counter=0
                    
                        # print("*****************did not attend******************")
                # attendance_status = 'attended' if attendance_records.filter(students_present=student, date=date.date).exists() else ''
                student_data['attendance_status'].append(attendance_status)
        attendance_data.append(student_data)
    
    # print("here ------------------ here ")
    # print(dates)
    # print("here ------------------ here ")
    # print(students[2])
    # print(attendance_records.filter(students_present=student, date=dates.first()).exists())
    # print(attendance_data[2])
    

    context = {
        'dates': dates,
        'attendance_data': attendance_data,

    }
    # print(dates[1])
    return render(request, 'project2/attendance_general.html', context)

@specific_username_required
def attendance_specific(request, class_number):
    if request.method == 'POST':
        
        attendance_data = AttendanceRecordForm(request.POST)
        attendance_data.instance.academic_year = class_number
        academic_year = request.POST.getlist('academic_year') 
        print("------------ everything faf -------------", academic_year)


        if attendance_data.is_valid():
            # print("------------ request post -------------", request.POST)
            attended_names = request.POST.getlist('attended_names')  # Assuming this is how you are getting the selected student names
            # print("------------ nothing faff -------------", attended_names)
            students_present = ','.join(attended_names)  # Convert the list of names to a comma-separated string
            # print("------------ everything faf -------------", students_present)
            academic_year = request.POST.getlist('academic_year')  # Convert the list of names to a comma-separated string
            # print("------------ everything faf -------------", academic_year)
            

            attendance_record = attendance_data.save(commit=False)  # Create the attendance record instance but don't save it yet
            attendance_record.students_present = students_present  # Assign the students_present value
            attendance_record.save()  # Now save the attendance record with the updated students_present value
            calculate_absences()
            return redirect('project2:attendance_general')
        else: 
            messages.error(request, f"form is invalid: date might exist once before.")

    form = AttendanceRecordForm()
    students_1 = None
    students_2 = None
    class_number = str(class_number)
    if class_number == "12":
        students_1= Student.objects.filter(academic_year__range=(-2,1))
        students_2= Student.objects.filter(academic_year=2)
    elif class_number == "34":
        students_1= Student.objects.filter(academic_year=3)
        students_2= Student.objects.filter(academic_year=4)
    elif class_number == "56":
        students_1= Student.objects.filter(academic_year=5)
        students_2= Student.objects.filter(academic_year=6)

    context = {
                'students_1': students_1, 
                'students_2': students_2, 
                'form': form, 
                'class_number': class_number
               }
    return render(request, "project2/attendance_specific.html", context)


@specific_username_required
def attendance_edit_specific(request, form_id):
    attendance_record = AttendanceRecord.objects.get(id=form_id)
    if request.method == 'POST':
        form = AttendanceRecordForm(request.POST, instance=attendance_record)
        attended_names = request.POST.getlist('attended_names')  # Assuming this is how you are getting the selected student names
        students_present = ','.join(attended_names)  # Convert the list of names to a comma-separated string
        attendance_record.students_present = students_present 
        attendance_record.day_title =  request.POST.get('day_title')
        attendance_record.day_topic =  request.POST.get('day_topic')
        attendance_record.day_verse =  request.POST.get('day_verse')
        attendance_record.day_notes =  request.POST.get('day_notes')
        

        attendance_record.save()
        calculate_absences()
        return redirect('project2:attendance_general')

    else:
        form = AttendanceRecordForm(instance=attendance_record)
    
    students_1 = None
    students_2 = None
    class_number = str(attendance_record.academic_year)
    if class_number == "12":
        students_1= Student.objects.filter(academic_year__range=(-2,1))
        students_2= Student.objects.filter(academic_year=2)
    elif class_number == "34":
        students_1= Student.objects.filter(academic_year=3)
        students_2= Student.objects.filter(academic_year=4)
    elif class_number == "56":
        students_1= Student.objects.filter(academic_year=5)
        students_2= Student.objects.filter(academic_year=6)

    context = {
                'students_1': students_1, 
                'students_2': students_2, 
                'form': form, 
               }
    

    return render(request, "project2/attendance_edit_specific.html", context)




@specific_username_required
def eftekad(request):

    # eftekad elsalah
    students_distress = Student.objects.filter(
    Q(father_alive=False) | Q(mother_alive=False) | ~Q(health_problems__exact=" ") & ~Q(health_problems__exact="") & ~Q(health_problems__exact="لا يوجد")
    )
    
    
    attendance_dates = AttendanceRecord.objects.filter(academic_year='12').order_by(F('date').desc()).distinct()
    last_attendance_date = attendance_dates.first()
    if last_attendance_date:
        present_students_names = last_attendance_date.students_present.split(",")
        students_attendance = Student.objects.filter(~Q(name__in=present_students_names) & Q(academic_year__range=(-2,2)))
    else:
        students_attendance = Student.objects.none()

    students_random = Choose_random_students(3)
    # students_queryset = Student.objects.all()  # Use .all() or other filtering methods to get a queryset
    # students_random = students_queryset[0:5]
    # students_random = 

    context = {
                'students_distress': students_distress,
                'students_random': students_random,
                'students_attendance': students_attendance,

                }
    
    return render(request, "project2/eftekad.html", context)