from django.db import models
from datetime import date
# from django.contrib.postgres.fields import ArrayField
from datetime import datetime


CLASS_CHOICES = (
    ("12", "12"),
    ("34", "34"),
    ("56", "56"),
)
GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )

# servants class
class Servant(models.Model):

    name = models.CharField(max_length=100, default="", blank=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default="male")
    phone_number = models.CharField(max_length=11, blank=True)
    phone_number2 = models.CharField(max_length=11, blank=True)
    
    home_town = models.CharField(max_length=255,default="منوف", blank=True)
    home_region = models.CharField(max_length=255,blank=True)
    home_address = models.CharField(max_length=255,blank=True)

    facebook_profile = models.CharField(max_length=255,blank=True)
    date_of_birth = models.DateField(default = date(2000, 1, 1), blank=True)

    class_number = models.CharField( max_length=10, choices=CLASS_CHOICES, blank=True)
    absences_number = models.IntegerField(default=0, blank=True, null=True)
    attendance_rate = models.FloatField(default=0.0, blank=True, null=True)
    def __str__(self):
        return self.name


# students class 
class Student(models.Model):
    
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
    SCHOOL_CHOICES = (
        # ("",""),
        ("الاسقفية","الاسقفية"),
        ("الاقباط الابتدائية","الاقباط الابتدائية"),
        ("التحرير","التحرير"),
        ("هابي سكول","هابي سكول"),
        ("برهيم التجريبية","برهيم التجريبية"),
        ("سدود التجريبية","سدود التجريبية"),
        ("الشيخ زويل","الشيخ زويل"),
        ("اخري","اخري"),
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
    school_name = models.CharField(max_length=255, choices=SCHOOL_CHOICES,blank=True)
    confession_father = models.CharField(max_length=15, choices=CONFESSION_FATHER_CHOICES, default="لا يوجد", blank=True)
    hobbies = models.CharField(max_length=255,blank=True)
    health_problems = models.CharField(max_length=255,default="لا يوجد", blank=True)
    home_town = models.CharField(max_length=255,default="منوف", blank=True)
    home_region = models.CharField(max_length=255,blank=True)
    home_address = models.CharField(max_length=255,blank=True)

    how_to_church = models.CharField(max_length=255,blank=True)
    registered_in_church_list = models.BooleanField(default=False)
    absences = models.IntegerField(default=0, blank=True, null=True)
    attendance_rate = models.FloatField(default=0.0, blank=True, null=True)
    responsible_servant = models.CharField(max_length=100, blank=True)

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
        # if not self.pk:  # Only perform these actions if the instance is being created, not updated
            # Check for other students with the same father name
            # other_students = Student.objects.filter(father_name=self.father_name).exclude(pk=self.pk)
            # for student in other_students:
            #     if student != self:
            #         # Establish brother relationship
            #         # student.brothers.add(self)
            #         # self.brothers.add(student)
            #         student.save()  # Save the related student
            #         self.save()     # Save the current student again with the added brother relationship
        if not self.father_name: 
            self.father_name = " ".join(student_name_parts[1:])
        if not self.mother_name:
            self.mother_name = f"ام {self.name}"
            # print("mother name is empty")
        # else: 
            # print("mother name is written ")

        super().save(*args, **kwargs)  # Save the initial instance


            

class AttendanceRecord(models.Model):
    
    DAY_TITLE_CHOICES = (
        ('مدارس احد', 'مدارس احد'),
        ('يوم روحي', 'يوم روحي'),
        ('خلوة', 'خلوة'),
        ('يوم رياضي', 'يوم رياضي'),
        ('رحلة', 'رحلة'),
        ('الحان', 'الحان'),
        ('تسبحة', 'تسبحة'),
        ('عشية', 'عشية'),
        ('عيد', 'عيد'),
        ('اخري', 'اخري')
    )

    date = models.DateField(default=datetime.today)
    day_title = models.CharField(max_length=50, choices=DAY_TITLE_CHOICES, default="مدارس احد")
    day_topic = models.CharField(max_length=255, default="", blank=True)
    day_verse = models.CharField(max_length=255, default="", blank=True)

    academic_year = models.CharField(max_length=30, choices=CLASS_CHOICES, default="", blank=True)
    class_attendance_rate = models.FloatField(default=0.0, blank=True)

    students_present = models.TextField(blank=True)
    students_eftekad_notyet = models.TextField(blank=True)

    servants_attended =models.TextField(blank=True)
    servants_eftekad_notyet = models.TextField(blank=True)

    day_notes = models.TextField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['date', 'academic_year', 'day_title'], name='unique_date_academic_year_day_title')
        ]
        

    # def mark_attendance(self, student):
    #     if not self.students_present:
    #         self.students_present = student.name
    #     else:
    #         self.students_present += f",{student.name}"

    # def get_attendance_list(self):
    #     if self.students_present:
    #         return self.students_present.split(",")
    #     return []

    # def get_date(self):
    #     return self.initial.get('date', None)

    def __str__(self):
        return f"Attendance for {self.academic_year}, {self.day_title} on {self.date}"
    
    def save_edits(self, students_present, day_title, day_topic, day_verse, day_notes):
        self.students_present = students_present
        self.day_title = day_title
        self.day_topic = day_topic
        self.day_verse = day_verse
        self.day_notes = day_notes
        
        # students_attended_number = len(self.students_present.split(","))
        # all_students_number = len(Student.objects.filter(academic_year__range=(-2,2)))
        # self.academic_year_attendance_rate = students_attended_number / all_students_number

        self.save()

    def save(self, *args, **kwargs):

        # calculate the attendance rate for each class
        students_attended_number = len(self.students_present.split(","))
        if self.academic_year== '12':
            all_students_number = len(Student.objects.filter(academic_year__range=(-2,2)))
        elif self.academic_year=="34":
            all_students_number = len(Student.objects.filter(academic_year__range=(3,4)))
        elif self.academic_year=="56":
            all_students_number = len(Student.objects.filter(academic_year__range=(5,6)))
            
        if all_students_number==0: 
            self.class_attendance = 0
        else:
            self.class_attendance_rate = round((students_attended_number / all_students_number)*100,1)

        super().save(*args, **kwargs)  # Save the initial instance
        