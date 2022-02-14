import datetime
import random
from hashlib import md5
import factory
from factory.fuzzy import FuzzyDate, FuzzyInteger

from django.conf import settings

from vmb.users.models import User
from . import models


PLACES_LIST = [
    "Mayapur, West Bengal, India, 23.4232013, 88.38826399999999",
    "Bangalore, Karnataka, India, 12.9715987, 77.5945627",
    "Pune, Maharashtra, India, 18.5204303, 73.8567437",
    "Mumbai, Maharashtra, India, 19.0759837, 72.8776559",
    "New Delhi, Delhi, India, 28.6139391, 77.2090212",
    "Kolkata, West Bengal, India, 22.572646, 88.36389500000001",
]

SPIRITUAL_MASTERS_IDS_LIST = [
    40,
    65,
    33,
    13,
]

MOTHER_TONGUE_CODES = [19, 107, 58, 84, 157, 156]


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "users.User"

    is_active = True
    password = "password12345"
    is_matrimony_candidate = True
    is_matrimony_registration_complete = True


def generate_profile_id(o):
    digest = (
        md5(
            f"{o.name}-{o.gender}-{o.phone}-{o.email}-{o.dob}-{o.phone}".encode("utf-8")
        )
        .hexdigest()[:7]
        .upper()
    )
    return f"{settings.PROFILE_ID_PREFIX}{digest}"


class MatrimonyProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "matrimony.MatrimonyProfile"

    id = factory.Sequence(lambda n: n)
    dob = FuzzyDate(datetime.date(1985, 1, 1), datetime.date(2002, 1, 1))
    profile_created_by = "SE"
    rounds_chanting = factory.Iterator([4, 8, 16])
    email = factory.Sequence(lambda n: "user_%d@example.com" % n)
    phone = factory.Sequence(lambda n: "999888%04d" % n)
    gender = factory.Iterator(["M", "F"])
    profile_id = factory.LazyAttribute(lambda o: generate_profile_id(o))
    user = factory.SubFactory(
        UserFactory,
        username=factory.SelfAttribute("..profile_id"),
        email=factory.SelfAttribute("..email"),
        name=factory.SelfAttribute("..name"),
        phone=factory.SelfAttribute("..phone"),
    )

    status = factory.Iterator(["00", "01", "20", "30"])
    mother_tongue = factory.Iterator(
        models.Language.objects.filter(id__in=MOTHER_TONGUE_CODES)
    )
    marital_status = factory.Iterator(
        [item[0] for item in models.profiles.MARITAL_STATUS]
    )
    ethnic_origin = factory.Iterator(models.Nationality.objects.filter(id__in=[57]))
    height = FuzzyInteger(145, 165)
    weight = FuzzyInteger(50, 90)
    body_type = factory.Iterator([item[0] for item in models.profiles.BODY_TYPE])
    complexion = factory.Iterator(
        [item[0] for item in models.profiles.COMPLEXION_CHOICES]
    )
    current_place = factory.Iterator(PLACES_LIST)
    birth_place = factory.Iterator(PLACES_LIST)

    @factory.lazy_attribute_sequence
    def name(self, n):
        return "%s %d" % ("Male" if self.gender == "M" else "Female", n)

    @factory.lazy_attribute
    def contact_person_name(self):
        return self.name

    @factory.lazy_attribute
    def current_city(self):
        return self.current_place.split(",")[0].strip()

    @factory.lazy_attribute
    def current_state(self):
        return self.current_place.split(",")[1].strip()

    @factory.lazy_attribute
    def current_country(self):
        return models.Country.objects.get(name=self.current_place.split(",")[2].strip())

    @factory.lazy_attribute
    def birth_city(self):
        return self.birth_place.split(",")[0].strip()

    @factory.lazy_attribute
    def birth_state(self):
        return self.birth_place.split(",")[1].strip()

    @factory.lazy_attribute
    def birth_country(self):
        return models.Country.objects.get(name=self.birth_place.split(",")[2].strip())

    @factory.post_generation
    def post(obj, create, extracted, **kwargs):
        expectations = obj.expectations
        expectations.age_from = obj.age + random.randint(-5, 0)
        expectations.age_to = obj.age + random.randint(0, 5)
        expectations.height_from = obj.height + random.randint(-5, 0)
        expectations.height_to = obj.height + random.randint(0, 5)

        expect_same_mother_tongue = random.randint(0, 1)
        if expect_same_mother_tongue:
            l = models.Language.objects.get(code=obj.mother_tongue.code)
            expectations.mother_tongues.add(l)

        expectations.save()
