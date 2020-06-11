import csv
import os
import re
import datetime 

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from vmb.matrimony.models.profiles import MatrimonyProfile
from vmb.matrimony.models import(
    Guru,
    Country,
    Expectation,
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

    MatrimonyProfile.objects.all().delete()

    for row in reader:
        print(row)

        dt= [int(i) for i in re.split(r'[.-/]',row[5]) if i.isdigit()]     
        new_dt= datetime.datetime.strptime(f"{dt[0]}-{dt[1]}-{dt[2]}", "%d-%m-%Y").date()

        if "Never Married" in row[10]:
            y_mar_sts = "UMR"
        else:
            y_mar_sts = row[10][0:3].upper()

        if row[12] == "YES":
            rounds = 16
        elif row[12] == "NO":
            rounds = 0
        else:
            rounds = row[12]
        
        
        if "First Initiated" in row[13]:
            y_s_status= "D1"
        elif "Second Initiated" in row[13]:
            y_s_status= "D2"
        else:
            y_s_status=row[13][0].upper() 

        if "Never Married" in row[19]:
            s_mar_sts = "UMR"
        else:
            s_mar_sts = row[10][0:3].upper()

        if row[33] != '' or row[33] is not None:
            wt = re.sub("\D", "", row[33])
        else:
            wt = row[33]

        if row[37]:
            y_income = [int(i) for i in row[37].split() if i.isdigit()][0]*12
        else:
            y_income = row[37] 

        if row[21]:
            s_income = [int(i) for i in row[21].split() if i.isdigit()]
            if len(s_income) == 1:
                s_income_f = s_income[0]
                s_income_t = None
            if len(s_income) == 2:
                s_income_f = s_income[0]
                s_income_t = s_income[1] 
        else:
            s_income_f = row[21] 
            s_income_t = None

        age_req= [int(i) for i in re.split(r'[-/\s]',row[16]) if i.isdigit()]  
        if len(age_req) == 1:
            age_f = age_req[0]
            age_t = None
        else:
            age_f = age_req[0]
            age_t = age_req[1]

        if row[45] is "YES" or row[45] is "NO":
            w_children = row[45][0].upper()
        else:
            w_children = "Mb"
    
        mp = MatrimonyProfile(
            name=row[1].title(),
            spiritual_name=row[2].title(),
            gender=row[3][0],
            dob=new_dt,
            email=row[8],
            marital_status=y_mar_sts,
            rounds_chanting=rounds,
            spiritual_status=y_s_status,
            annual_income=y_income,
            weight=wt,
            # hair_color=row[34],
            # color_of_hair=row[35],
            personality = row[38],
            recreational_activities = row[41],
            devotional_services = row[42],
            medical_history = row[44],
            want_children = w_children,
        )
        mp.save()
        e = Expectation(
            profile=mp,
            age_from=age_f,
            age_to=age_t,
            marital_status=s_mar_sts,
            partner_description=row[28],
            annual_income_from=s_income_f,
            annual_income_to=s_income_t,
        )
        e.save()