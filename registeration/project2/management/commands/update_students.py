from django.core.management.base import BaseCommand
from project2.models import Student

class Command(BaseCommand):
    help = 'Update is_active field for all students instances'

    def handle(self, *args, **options):
        Student.objects.update(father_alive=True)
        Student.objects.update(mother_alive=True)
        self.stdout.write(self.style.SUCCESS('Updated is_active for all students instances'))