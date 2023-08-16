import pandas as pd
from project2.models import Student
import math


header_to_field_mapping = {
    'الاسم': 'name',
    'النوع': 'gender',
    'السنة الدراسية': 'academic_year',
    'رقم التليفون': 'phone_number',
    'رقم التليفون 2': 'phone_number2',
    'اسم الايميل': 'facebook_profile',
    # 'Arabic_Header_2': 'date_of_birth',
    'اليوم': 'day_of_birth',                    # to be converted and deleted
    'الشهر': 'month_of_birth',                  # to be converted and deleted
    'سنة الميلاد': 'year_of_birth',             # to be converted and deleted
    'ايميل الفيسبوك': 'facebook_link',         # to be deleted
    'مجالات الانترنت': 'internet_usage',        # to be deleted
    'ملاحظات علي الطفل': 'notes',
    'اسم المدرسة': 'school_name',
    'اسم اب الاعتراف': 'confession_father',
    'هوايات': 'hobbies',
    'مشاكل صحية': 'health_problems',
    'البلد': 'home_town',
    'المنطقة': 'home_region',
    'العنوان': 'home_address',
    'طريقة الوصول للكنيسة': 'how_to_church',
    'موجود بكشف الكنيسة': 'registered_in_church_list',
    'الغياب': 'absences',
    'اخواته': 'brothers',

    'اسم الاب': 'father_name',
    'رقم تليفون الاب': 'father_phone_number1',
    'رقم تليفون الاب 2': 'father_phone_number2',
    'ايميل الاب': 'father_facebook_link',       # to be deleted
    'اسم ايميل الاب': 'father_facebook_profile',
    'وظيفة الاب': 'father_job',
    'الاب علي قيد الحياة': 'father_alive',
    'ملاحظات علي الاب': 'father_notes',

    'اسم الام': 'mother_name',
    'رقم تليفون الام': 'mother_phone_number1',
    'رقم تليفون الام 2': 'mother_phone_number2',
    'ايميل الام ': 'mother_facebook_link',      # to be deleted
    'اسم ايميل الام': 'mother_facebook_profile',
    'وظيفة الام': 'mother_job',
    'الام علي قيد الحياة': 'mother_alive',
    'ملاحظات عن الام': 'mother_notes',
    # Add more mappings as needed
}

columns_to_drop = ['day_of_birth', 
                   'month_of_birth', 
                   'year_of_birth', 
                   'facebook_link', 
                   'internet_usage', 
                   'father_facebook_link', 
                   'mother_facebook_link', 
                   'brothers',
                   ]

def read_excel_file(file_path, sheet_name):
    data = pd.read_excel(file_path, sheet_name=sheet_name)
    data.rename(columns=header_to_field_mapping, inplace=True)
    return data

def validate_datatypes(excel_data):

    for index, row in excel_data.iterrows():
        for column_name in excel_data.columns:
            if pd.isna(row[column_name]):
                excel_data.at[index, column_name] = ''
        # Map Arabic gender values to match Django model's GENDER_CHOICES
        arabic_gender = row['gender']
        if 'ولد' in arabic_gender:
            excel_data.at[index, 'gender'] = 'male'
        else:
            excel_data.at[index, 'gender'] = 'female'

        # Convert academic_year to integer
        # excel_data.at[index, 'academic_year'] = 1

        # Convert phone numbers to strings

        # if math.isnan(excel_data.at[index, 'phone_number']):
        #     excel_data.at[index, 'phone_number'] = ''
        # else:  excel_data.at[index, 'phone_number'] = '0'+str(row['phone_number'])[:-2]
        # if math.isnan(excel_data.at[index, 'phone_number2']):
        #     excel_data.at[index, 'phone_number2'] = ''
        # else:  excel_data.at[index, 'phone_number2'] = '0'+str(row['phone_number2'])[:-2]
        # if math.isnan(excel_data.at[index, 'father_phone_number1']):
        #     excel_data.at[index, 'father_phone_number1'] = ''
        # else:  excel_data.at[index, 'father_phone_number1'] = '0'+str(row['father_phone_number1'])[:-2]
        # if math.isnan(excel_data.at[index, 'father_phone_number2']):
        #     excel_data.at[index, 'father_phone_number2'] = ''
        # else:  excel_data.at[index, 'father_phone_number2'] = '0'+str(row['father_phone_number2'])[:-2]
        # if math.isnan(excel_data.at[index, 'mother_phone_number1']):
        #     excel_data.at[index, 'mother_phone_number1'] = ''
        # else:  excel_data.at[index, 'mother_phone_number1'] = '0'+str(row['mother_phone_number1'])[:-2]
        # if math.isnan(excel_data.at[index, 'mother_phone_number2']):
        #     excel_data.at[index, 'mother_phone_number2'] = ''
        # else:  excel_data.at[index, 'mother_phone_number2'] = '0'+str(row['mother_phone_number2'])[:-2]
        excel_data.at[index, 'phone_number'] = '0'+str(row['phone_number'])[:-2]
        excel_data.at[index, 'phone_number2'] = '0'+str(row['phone_number2'])[:-2]
        excel_data.at[index, 'father_phone_number1'] = '0'+str(row['father_phone_number1'])[:-2]
        excel_data.at[index, 'father_phone_number2'] = '0'+str(row['father_phone_number2'])[:-2]
        excel_data.at[index, 'mother_phone_number1'] = '0'+str(row['mother_phone_number1'])[:-2]
        excel_data.at[index, 'mother_phone_number2'] = '0'+str(row['mother_phone_number2'])[:-2]

        # Convert boolean fields to boolean values
        excel_data.at[index, 'father_alive'] = row['father_alive'] == 'نعم'
        excel_data.at[index, 'mother_alive'] = row['mother_alive'] == 'نعم'
        excel_data.at[index, 'registered_in_church_list'] = row['registered_in_church_list'] == 'نعم'

        # Convert absences to integer
        excel_data.at[index, 'absences'] = int(row['absences'])

        # Convert date_of_birth to datetime if not NaN
        if pd.notnull(row['date_of_birth']):
            date_str = row['date_of_birth']
            excel_data.at[index, 'date_of_birth'] = pd.to_datetime(date_str, errors='coerce')

        excel_data.at[index, 'brothers'] = []  # Assign an empty list

        excel_data.at[index, 'notes'] = str(row['notes'])

        # print(index)
        # print(type(row['brothers']))

    return excel_data
