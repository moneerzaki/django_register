from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'  # You can specify the fields you want to include here if needed
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            # Add more widgets as needed
        }

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)

        self.fields['mother_notes'].widget.attrs.update({'rows': 2}) 
        self.fields['father_notes'].widget.attrs.update({'rows': 2}) 




# class GuardianForm(forms.ModelForm):
#     class Meta:
#         model = Guardian
#         fields = '__all__'  # You can specify the fields you want to include here if needed