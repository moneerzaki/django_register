from django.core.management.base import BaseCommand
from project2.models import Servant  # Import your Django model
# from excel_importer import header_to_field_mapping, columns_to_drop
from excel_importer import servants_header_to_field_mapping
import pandas as pd



class Command(BaseCommand):
    help = 'Import servants data from Excel file'
    file_path = r"C:\Users\monee\Desktop\moneer\elkhedma\بيانات خدام ابتدائي.xlsx"  # Define the file path here
    sheet_name = "Sheet1"  # Define the sheet name here
    # table_name = "Table6"  # Define the name of the table you want to read
    start_row = 1  # The row where the table starts (adjust as needed)
    end_row = 7  # The row where the table ends (None means read until the end)



    def handle(self, *args, **options):
        from excel_importer import validate_datatypes  # Import the functions you created
        # Read Excel data and perform data transformations
        excel_data = self.read_table_from_excel()

        # excel_data = validate_datatypes(excel_data)
        
        print(excel_data)
        # print(excel_data.columns)

        Servant.objects.all().delete()
        for index, row in excel_data.iterrows():
            # Create Student instance
            servant = Servant(**row)
            servant.save()

        self.stdout.write(self.style.SUCCESS('Servants Data imported successfully.'))


    def read_table_from_excel(self):
        data = pd.read_excel(self.file_path, sheet_name=self.sheet_name, header=self.start_row - 1, nrows=self.end_row)
        data.rename(columns=servants_header_to_field_mapping, inplace=True)
        return data