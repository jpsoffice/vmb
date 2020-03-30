import csv
import os

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from matrimony.models import MatrimonyProfile, Guru, Country, Nationality, Language, Degree, Occupation

BASE = os.path.dirname(os.path.abspath(__file__))

class Command(BaseCommand):
    help = 'Closes the specified matrimony profile for voting'

    def add_arguments(self, parser):
        parser.add_argument("file", type=str)

    def handle(self, *args, **options):
        run(options["file"])


def run(file_path):
    csv_file = open(os.path.join(BASE, file_path))
    reader = csv.reader(csv_file)

    next(reader)

    MatrimonyProfile.objects.all().delete()

    for row in reader:
        print(row)
    
        g, created = Guru.objects.get_or_create(name=row[4])
        d, created = Degree.objects.get_or_create(degree=row[16])
        o, created = Occupation.objects.get_or_create(occupation=row[17])

        mp = MatrimonyProfile(name=row[0], gender=row[1], rounds_chanting=row[2], 
            s_status=row[3], guru=g, dob=row[5], tob=row[6], birth_city=row[7], 
            current_city=row[10], height=row[14], degree=d, occupation=o,
            annual_income=row[18], marital_status=row[19], email_id=row[20], phone=row[21], 
            expectations=row[22])
        mp.save()


