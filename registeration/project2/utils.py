from django.db.models import Q, F   
from .models import Student
from .models import AttendanceRecord
from datetime import datetime, timedelta
from django.core.cache import cache
import random


def calculate_absences():


    attendance_dates = AttendanceRecord.objects.filter(academic_year='12').order_by(F('date').desc()).distinct()
    Student.objects.all().update(absences=0)


    # calculate the number of absences since last time
    last_attendance_date = attendance_dates.first()
    if last_attendance_date:
        present_students_names = last_attendance_date.students_present.split(",")
        students_attendance_initial = Student.objects.filter(~Q(name__in=present_students_names) & Q(academic_year__range=(-2,2)))
    else:
        students_attendance_initial = Student.objects.none()
    
    for attendance_date in attendance_dates: 
        present_students_names = attendance_date.students_present.split(",")
        for student in students_attendance_initial:
            if student.name in present_students_names:
                # print ( "***************** ", student.name, " ******************* ")
                student.save()
                students_attendance_initial = students_attendance_initial.exclude(id=student.id)
            else: 
                student.absences +=1
                student.save()


    # calculate the attendance_rate 
    students = Student.objects.all()
    total_attendances = len(attendance_dates)
    print("((((((((((((((((()))))))))))))))))", total_attendances)
    for student in students:
        count=0.0
        if total_attendances: 
            for attendance_date in attendance_dates:
                present_students_names = attendance_date.students_present.split(",")
                if student.name in present_students_names:
                    count += 1
                if student.name == "شنودة ميشيل" and student.name not in present_students_names:
                    print("+++++++++ date: ", attendance_date.date, " day_title", attendance_date.day_title )
            # attendance_rate = round((count/total_attendances) * 100, 1)
        if total_attendances ==0: 
            student.attendance_rate = 0
        else: 
            student.attendance_rate = round((count/total_attendances) * 100, 1)

        student.save()

    return 


def Choose_random_students(students_number):

    
    all_student_ids = Student.objects.values_list('id', flat=True)
    random_student_ids = random.sample(list(all_student_ids), students_number)
    random_students = Student.objects.filter(id__in=random_student_ids)

    
    return random_students
    
# def Choose_random_students(students_number):
#     # Define a key for storing the last execution timestamp in the cache
#     cache_key = 'last_execution_timestamp'
    
#     # Retrieve the last execution timestamp from the cache
#     last_execution_timestamp = cache.get(cache_key)
    
#     # Get the current timestamp
#     current_timestamp = datetime.now()
    
#     # Calculate the start and end of the current day
#     current_day_start = current_timestamp.replace(hour=0, minute=0, second=0, microsecond=0)
#     current_day_end = current_timestamp.replace(hour=23, minute=59, second=59, microsecond=999999)
    
#     # If the function hasn't been run today, execute it and update the cache
#     if not last_execution_timestamp or not (current_day_start <= last_execution_timestamp <= current_day_end):
#         all_student_ids = Student.objects.values_list('id', flat=True)
#         random_student_ids = random.sample(list(all_student_ids), students_number)
#         random_students = Student.objects.filter(id__in=random_student_ids)
        
#         # Update the last execution timestamp in the cache
#         # cache.set(cache_key, current_timestamp, timedelta(days=1))
        
#         return random_students
    
#     return None  # Function has already been run today