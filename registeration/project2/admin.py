from django.contrib import admin
from .models import Student
from .models import AttendanceRecord
from .models import Servant

# Register your models here.
admin.site.register(Student)
admin.site.register(AttendanceRecord)
admin.site.register(Servant)