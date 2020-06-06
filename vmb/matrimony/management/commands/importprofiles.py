import csv
import os

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from vmb.matrimony.models import (
    Guru,
    Country,
    Nationality,
    Language,
    Occupation,
    Male,
    Female,
    OccupationCategory, 
    Education, 
    EducationCategory,
    Religion,
    Caste,
    Subcaste,
)

BASE = os.path.dirname(os.path.abspath(__file__))


class Command(BaseCommand):
    help = "Closes the specified matrimony profile for voting"

    def add_arguments(self, parser):
        parser.add_argument("file", type=str)

    def handle(self, *args, **options):
        run(options["file"])


def run(file_path):
    csv_file = open(os.path.join(BASE, file_path))
    reader = csv.reader(csv_file)

    next(reader)

    # MatrimonyProfile.objects.all().delete()
    # Male.objects.all().delete()
    # Female.objects.all().delete()


    for row in reader:
        print(row)

        dt=row[5].split("/ |- |.")
        new_dt= datetime.datetime.strptime(f"{dt[0]}-{dt[1]}-{dt[2]}", "%d-%m-%Y").date()

        if row[10]="Never Married":
            mar_sts = "UMR"
        elif row[10]="Divorced":
            mar_sts ="DIV"
        elif row[10]="Widow":
            mar_sts ="WID"
        else:
            mar_sts ="SEP"

        if row[12] = "YES"
            rounds = 16
        elif row[12] = "NO":
            rounds = 0
        else:
            rounds = row[12]
        

        if row[3].title() = 'Male':

            male = Male(
                name=row[1].title(),
                spiritual_name=row[2].title(),
                dob=new_dt,
                email=row[8],
                # rounds_chanting=row[],
                s_status=row[3],
                guru=g,
                tob=row[6],
                birth_city=row[7],
                current_city=row[10],
                height=row[14],
                degree=d,
                occupation=o,
                monthly_income=row[18],
                marital_status=row[19],
                email_id=row[20],
                phone=row[21],
                expectations=row[22],
            )
            male.save()

        else:
            female = Female(
                    name=row[0],
                    gender=row[1],
                    rounds_chanting=row[2],
                    s_status=row[3],
                    guru=g,
                    dob=row[5],
                    tob=row[6],
                    birth_city=row[7],
                    current_city=row[10],
                    height=row[14],
                    degree=d,
                    occupation=o,
                    monthly_income=row[18],
                    marital_status=row[19],
                    email_id=row[20],
                    phone=row[21],
                    expectations=row[22],
                )
                female.save()
