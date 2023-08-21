from django.db import models
from datetime import date
# from django.contrib.postgres.fields import ArrayField
from datetime import datetime



class Student(models.Model):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    CONFESSION_FATHER_CHOICES = (
        ('لا يوجد', 'لا يوجد'),
        ('ابونا تاردس', 'ابونا تادرس'),
        ('ابونا سيرافيم', 'ابونا سيرافيم'),
        ('ابونا تيمثاوس', 'ابونا تيمثاوس'),
        ('اب كاهن اخر', 'اب كاهن اخر'),
    )

    ACADEMIC_YEAR_CHOICES = (
        (-2, '-2'),
        (-1, '-1'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
    )


    #required fields
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default="male")
    academic_year = models.IntegerField(choices=ACADEMIC_YEAR_CHOICES)

    #non-required fields.
    phone_number = models.CharField(max_length=11, blank=True)
    phone_number2 = models.CharField(max_length=11, blank=True)
    facebook_profile = models.CharField(max_length=255,blank=True)
    date_of_birth = models.DateField(default = date(2000, 1, 1), blank=True)
    school_name = models.CharField(max_length=255,blank=True)
    confession_father = models.CharField(max_length=15, choices=CONFESSION_FATHER_CHOICES, default="لا يوجد", blank=True)
    hobbies = models.CharField(max_length=255,blank=True)
    health_problems = models.CharField(max_length=255,default="لا يوجد", blank=True)
    home_town = models.CharField(max_length=255,default="منوف", blank=True)
    home_region = models.CharField(max_length=255,blank=True)
    home_address = models.CharField(max_length=255,blank=True)
    how_to_church = models.CharField(max_length=255,blank=True)
    registered_in_church_list = models.BooleanField(default=False)
    absences = models.IntegerField(default=0, blank=True, null=True)
    brothers = models.ManyToManyField('self', symmetrical=True, blank=True, default=list)
    notes = models.TextField(blank=True, default='')


    #GUARDIANS parts
    father_name = models.CharField(max_length=100,blank=True)
    father_phone_number1 = models.CharField(max_length=11, blank=True)
    father_phone_number2 = models.CharField(max_length=11, blank=True)
    father_facebook_profile = models.CharField(max_length=255,blank=True)
    father_job = models.CharField(max_length=100, blank=True)
    father_alive = models.BooleanField(default=True)
    father_notes = models.TextField(blank=True)

    mother_name = models.CharField(max_length=100,blank=True)
    mother_phone_number1 = models.CharField(max_length=11, blank=True)
    mother_phone_number2 = models.CharField(max_length=11, blank=True)
    mother_facebook_profile = models.CharField(max_length=255,blank=True)
    mother_job = models.CharField(max_length=100, blank=True)
    mother_alive = models.BooleanField(default=True)
    mother_notes = models.TextField(blank=True)


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        student_name_parts = self.name.split()
        if not self.pk:  # Only perform these actions if the instance is being created, not updated
            if self.name:
                self.father_name = " ".join(student_name_parts[1:])
                self.mother_name = f"ام {self.name}"

            super().save(*args, **kwargs)  # Save the initial instance

            # Check for other students with the same father name
            other_students = Student.objects.filter(father_name=self.father_name).exclude(pk=self.pk)
            for student in other_students:
                if student != self:
                    # Establish brother relationship
                    student.brothers.add(self)
                    self.brothers.add(student)
                    student.save()  # Save the related student
                    self.save()     # Save the current student again with the added brother relationship

            

class AttendanceRecord(models.Model):
    date = models.DateField(default=datetime.today)
    day_title = models.CharField(max_length=30, default="مدارس احد")
    academic_year=models.CharField(max_length=30, default="", blank=True)
    students_present = models.TextField(blank=True)

    def mark_attendance(self, student):
        if not self.students_present:
            self.students_present = student.name
        else:
            self.students_present += f",{student.name}"

    def get_attendance_list(self):
        if self.students_present:
            return self.students_present.split(",")
        return []

    def __str__(self):
        return f"Attendance for {self.day_title} on {self.date}"
