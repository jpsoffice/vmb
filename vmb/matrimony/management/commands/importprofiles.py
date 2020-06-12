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
            if dt[2] > 20:
                dt[2] = 1900 + dt[2]
            else:
                dt[2] = 2000 + dt[2]
        new_dt = datetime.datetime.strptime(
            f"{dt[0]}-{dt[1]}-{dt[2]}", "%d-%m-%Y"
        ).date()
    else:
        new_dt = None
    return new_dt


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
    if a != "" or a is not None:
        wt = re.sub("\D", "", a)
    else:
        wt = a
    return wt


def get_annual_income(a):
    income = [int(i) for i in a.split() if i.isdigit()]
    if len(income) >= 1:
        if "USD" in income or "usd" in income or "Usd" in income:
            currency = "USD"
        else:
            currency = "INR"
        income = income[0] * 12
        the_income = Money(income, currency)
    else:
        the_income = None
    return the_income


def get_spouse_income(a):
    if a:
        income = [int(i) for i in a.split() if i.isdigit()]
        if "USD" in a or "usd" in a or "Usd" in a:
            currency = "USD"
        else:
            currency = "INR"
        if len(income) == 1:
            income_f = Money(income[0] * 12, currency)
            income_t = None
        if len(income) == 2:
            income_f = Money(income[0] * 12, currency)
            income_t = Money(income[1] * 12, currency)
    else:
        income_f = None
        income_t = None
    return income_f, income_t


def get_spouse_age(a):
    age = [int(i) for i in re.split(r"[-/\s]", row[16]) if i.isdigit()]
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

    for obj in MatrimonyProfile.objects.all():
        if obj.id != 25:
            obj.delete()

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
        # print(mp.spiritual_status)
        mp.save()
        # e = Expectation(
        #     profile=mp,
        #     age_from=get_spouse_age(row[16])[0],
        #     age_to=get_spouse_age(row[16])[1],
        #     marital_status=get_marital_status(row[19]),
        #     partner_description=row[28],
        #     spiritual_status=get_spiritual_status(row[22])

        # annual_income_from=get_spouse_income(row[21])[0],
        # annual_income_to=get_spouse_income(row[21])[1],
        # )
        # e.save()
