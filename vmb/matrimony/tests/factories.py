import factory
from faker import Faker
from django.contrib.auth import get_user_model
from vmb.matrimony.models import *
from django.contrib.auth.hashers import make_password
from random import randint, randrange
import datetime

fake = Faker()

class UserCustomFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = fake.user_name()
    password = make_password('wordpass123')
    email = fake.email()
    phone = randint(1000000000,9999999999)
    is_active = True

class MatrimonyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MatrimonyProfile

    name = fake.name()
    user =  factory.SubFactory(UserCustomFactory)
    profile_id = fake.user_name()
    contact_person_name=fake.name()
    profile_created_by=['SE','PA','SI','CO','FR'][randint(0,4)]
    gender=['M','F','O'][randint(0,2)]
    status='00'
    marital_status= ['UMR','WID','DIV'][randint(0,2)]
    rounds_chanting=25
    dob=datetime.datetime.strptime('14/12/2000', "%d/%m/%Y")