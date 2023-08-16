from django.core.management.base import BaseCommand
from project2.models import Student  # Import your Django model
from excel_importer import header_to_field_mapping, columns_to_drop
import pandas as pd



class Command(BaseCommand):
    help = 'Import data from Excel file'
    file_path = r"C:\Users\monee\Desktop\moneer\elkhedma\بيانات ابتدائي + اعدادي + ثانوي.xlsx"  # Define the file path here
    sheet_name = "Sheet1"  # Define the sheet name here
    # table_name = "Table6"  # Define the name of the table you want to read
    start_row = 1  # The row where the table starts (adjust as needed)
    end_row = 77  # The row where the table ends (None means read until the end)



    def handle(self, *args, **options):
        from excel_importer import read_excel_file, validate_datatypes  # Import the functions you created
        # Read Excel data and perform data transformations
        excel_data = self.read_table_from_excel()
        # excel_data = read_excel_file(file_path=self.file_path, sheet_name = self.sheet_name)
        
        # add missing columns
        excel_data['date_of_birth'] = excel_data['year_of_birth'].astype(str) + '-' + excel_data['month_of_birth'].astype(str) + '-' + excel_data['day_of_birth'].astype(str)

        #remove extra columns
        excel_data.drop(columns=columns_to_drop, inplace=True)

        #readd missing columns
        excel_data['brothers'] = ''

        excel_data = validate_datatypes(excel_data)
        

        # print(excel_data)
        # print(excel_data.columns)

        Student.objects.all().delete()
        for index, row in excel_data.iterrows():
            # Create Student instance
            student = Student(**{k: v for k, v in row.items() if k != 'brothers'})
            student.save()

        self.stdout.write(self.style.SUCCESS('Data imported successfully.'))


    def read_table_from_excel(self):
        data = pd.read_excel(self.file_path, sheet_name=self.sheet_name, header=self.start_row - 1, nrows=self.end_row)
        data.rename(columns=header_to_field_mapping, inplace=True)
        return data