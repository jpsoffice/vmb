import csv
import os
import re
import datetime


from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from djmoney.money import Money
from vmb.matrimony.models.profiles import MatrimonyProfile
from vmb.matrimony.models import (
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


def get_dob(a):
    dt = [int(i) for i in re.split(r"[./-]", a) if i.isdigit()]
    if len(dt) is 3:
        if dt[2] < 100:
            if dt[2] > datetime.datetime.now().year - 18 - 2000:
                dt[2] = 1900 + dt[2]
            else:
                dt[2] = 2000 + dt[2]
        new_dt = datetime.datetime.strptime(
            f"{dt[0]}-{dt[1]}-{dt[2]}", "%d-%m-%Y"
        ).date()
    return new_dt if new_dt else None


def get_marital_status(a):
    if "Never Married" in a:
        mar_sts = "UMR"
    else:
        mar_sts = a[0:3].upper()
    return mar_sts


def get_rounds_chanting(a):
    if a == "YES":
        rounds = 16
    elif a == "NO":
        rounds = 0
    else:
        rounds = a
    return rounds


def get_spiritual_status(a):
    if "First Initiated" in a:
        s_status = "D1"
    elif "Second Initiated" in a:
        s_status = "D2"
    else:
        s_status = a[0].upper()
    return s_status


def get_weight(a):
    try:
        if a or a != "" or a is not None:
            wt = re.sub("\D", "", a)
    except ValueError:
        pass
    return wt if wt else 0


def get_annual_income(a):
    income = re.sub("\D", "", a)
    if income:
        if "usd" in a.lower():
            currency = "USD"
        else:
            currency = "INR"
        income = int(income) * 12
        the_income = Money(income, currency)
    else:
        the_income = None
    return the_income


def get_spouse_age(a):
    age = [int(i) for i in re.split(r"[-/\s]", a) if i.isdigit()]
    if len(age) == 1:
        age_f = age[0]
        age_t = None
    else:
        age_f = age[0]
        age_t = age[1]
    return age_f, age_t


def get_want_children(a):
    if a is "YES" or a is "NO":
        want_children = a[0].upper()
    else:
        want_children = "Mb"
    return want_children


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

        mp = MatrimonyProfile(
            name=row[1].title(),
            spiritual_name=row[2].title(),
            gender=row[3][0],
            dob=get_dob(row[5]),
            email=row[8],
            marital_status=get_marital_status(row[10]),
            rounds_chanting=get_rounds_chanting(row[12]),
            spiritual_status=get_spiritual_status(row[13]),
            annual_income=get_annual_income(row[37]),
            weight=get_weight(row[33]),
            # hair_color=row[34],
            # color_of_hair=row[35],
            personality=row[38],
            recreational_activities=row[41],
            devotional_services=row[42],
            medical_history=row[44],
            want_children=get_want_children(row[45]),
        )
        mp.save()
        spouse_age = get_spouse_age(row[16])
        e = Expectation(
            profile=mp,
            age_from=spouse_age[0],
            age_to=spouse_age[1],
            marital_status=get_marital_status(row[19]),
            partner_description=row[28],
            spiritual_status=get_spiritual_status(row[22]),
            annual_income_from=get_annual_income(row[21]),
            annual_income_to=None,
        )
        e.save()
