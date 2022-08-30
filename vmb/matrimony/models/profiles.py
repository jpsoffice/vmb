import datetime
from dateutil.relativedelta import relativedelta
from hashlib import md5

from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.shortcuts import reverse
from django.template import loader, Context
from django.utils.html import format_html
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from djmoney.contrib.exchange.models import convert_money
from places.fields import PlacesField
from post_office import mail

from vmb.common.utils import build_absolute_url
from vmb.metrics import count
from vmb.users.models import User
from djmoney.models.fields import MoneyField
from djmoney.models.managers import money_manager
from multiselectfield import MultiSelectField

from .base import BaseModel
from .relations import (
    Occupation,
    Education,
    Guru,
    Language,
    Country,
    Nationality,
    Religion,
    Caste,
    Subcaste,
    Gotra,
)

FATHER_STATUS_CHOICES = (
    ("EMP", "Employed"),
    ("BUS", "Business"),
    ("PRO", "Professional"),
    ("RET", "Retired"),
    ("NMP", "Not Employed"),
    ("DEC", "Deceased"),
)
MOTHER_STATUS_CHOICES = (
    ("HMK", "Home Maker"),
    ("EMP", "Employed"),
    ("BUS", "Business"),
    ("PRO", "Professional"),
    ("RET", "Retired"),
    ("NMP", "Not Employed"),
    ("DEC", "Deceased"),
)
ARE_PARENTS_DEV = (
    ("Y", "Yes"),
    ("N", "No"),
    ("OF", "Only Father"),
    ("OM", "Only Mother"),
)
COLOR_OF_EYES = (
    ("AMB", "Amber"),
    ("BLU", "Blue"),
    ("BRW", "Brown"),
    ("GRY", "Gray"),
    ("GRN", "Green"),
    ("HAZ", "Hazel"),
    ("RED", "Red"),
)
HAIR_COLOR = (
    ("BRW", "Brown"),
    ("BLN", "Blond"),
    ("BLK", "Black"),
    ("RED", "Red"),
    ("WHT", "White"),
)
PROFILE_CREATED_BY_CHOICES = (
    ("SE", "Self"),
    ("PA", "Parent"),
    ("SI", "Sibling"),
    ("CO", "Counselor"),
    ("FR", "Friend"),
)
PROFILE_STATUS_CHOICES = (
    ("00", "Signup"),
    ("01", "Registered"),
    ("02", "Need more info"),
    ("10", "Inactive"),
    ("11", "Blocked"),
    ("20", "Active"),
    ("30", "In progress"),
    ("40", "Matched"),
    ("50", "QA"),
    ("60", "Discussions"),
    ("90", "Married externally"),
    ("99", "Married"),
)
PROFILE_STATUS_CHOICES_DICT = dict(PROFILE_STATUS_CHOICES)
BODY_TYPE = (
    ("SLM", "Slim"),
    ("AVG", "Average"),
    ("ATH", "Athelete"),
    ("HEA", "Heavy"),
)
GENDER_CHOICES = (("M", "Male"), ("F", "Female"), ("O", "Others"))
SPIRITUAL_STATUS_CHOICES = (
    ("A", "Aspiring"),
    ("S", "Shelter"),
    ("D1", "Harinam"),
    ("D2", "Brahmin"),
    ("NA", "Not Applicable"),
)
EMPLOYED_IN_CHOICES = (
    ("PSU", _("Government/PSU")),
    ("PVT", _("Private")),
    ("BUS", _("Business")),
    ("DEF", _("Defence")),
    ("SE", _("Self Employed")),
    ("NW", _("Not Working")),
)
FAMILY_LOCATION_CHOICES = (
    ("SAME", _("Same as my location")),
    ("DIFFERENT", _("Different Location")),
)
FAMILY_VALUE_CHOICES = (
    ("ORTH", _("Orthodox")),
    ("TRAD", _("Traditional")),
    ("MOD", _("Moderate")),
    ("LIB", _("Liberal")),
)
FAMILY_TYPE_CHOICES = (
    ("JF", _("Joint Family")),
    ("NF", _("Nuclear Family")),
    ("OTH", _("Others")),
)
FAMILY_STATUS_CHOICES = (
    ("LC", _("Lower Class")),
    ("UC", _("Upper Class")),
    ("MC", _("Upper Middle Class")),
    ("AF", _("Affluent")),
)
COMPLEXION_CHOICES = (
    ("FAI", _("Fair")),
    ("VFA", _("Very fair")),
    ("WHT", _("Wheatish")),
    ("WHB", _("Wheatish brown")),
    ("DAR", _("Dark")),
)

MARITAL_STATUS = (
    ("UMR", "Unmarried"),
    ("DIV", "Divorced"),
    ("WID", "Widowed"),
)
Y_N_MAYB = (
    ("Y", "Yes"),
    ("N", "No"),
    ("", "May be"),
)
CHILDREN_COUNT = (
    (0, "0"),
    (1, "1"),
    (2, "2"),
    (3, "3"),
)

BOOL_YES_NO = (
    (True, "Yes"),
    (False, "No"),
)


class MatrimonyProfile(BaseModel):
    """Model representing matrimonial profile of a candidate"""

    profile_id = models.CharField(max_length=15, blank=True, unique=True)
    registration_date = models.DateTimeField(default=timezone.now, blank=True)
    name = models.CharField(max_length=200, verbose_name=_("Name"),)
    spiritual_name = models.CharField(
        max_length=200, default="", blank=True, verbose_name=_("Spiritual name")
    )
    contact_person_name = models.CharField(
        max_length=200, verbose_name=_("Contact person name"), default=""
    )
    profile_created_by = models.CharField(
        max_length=2, choices=PROFILE_CREATED_BY_CHOICES, default="SE"
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,)
    status = models.CharField(
        max_length=2, choices=PROFILE_STATUS_CHOICES, blank=True, default="00"
    )
    marital_status = models.CharField(max_length=3, choices=MARITAL_STATUS, null=True,)
    children_count = models.PositiveIntegerField(
        choices=CHILDREN_COUNT, default=0, blank=True, null=True
    )
    ethnic_origin = models.ForeignKey(
        Nationality,
        on_delete=models.SET_NULL,
        null=True,
        related_name="ethnic_origin",
        blank=True,
    )

    photos = models.ManyToManyField("photologue.Photo", through="Photo", blank=True)
    photos_visible_to_all_matches = models.BooleanField(
        default=True,
        blank=True,
        null=True,
        help_text="By default, your photos will be visible to all suggested matches. If you uncheck this option, your photos will only be visible to matches you have accepted.",
    )

    # Contact details
    email = models.EmailField(null=True, unique=True, verbose_name=_("Email"))
    phone = models.CharField(max_length=17, unique=True, verbose_name=_("Phone number"))

    # Spiritual details
    rounds_chanting = models.PositiveIntegerField(
        verbose_name=_("Rounds"),
        help_text="How many rounds are you chanting?",
        default=0,
    )
    spiritual_status = models.CharField(
        max_length=2,
        help_text="Enter spiritual status (e.g. Aspiring, Shelter etc.)",
        choices=SPIRITUAL_STATUS_CHOICES,
        verbose_name=_("Spiritual Status"),
        blank=True,
    )
    spiritual_master = models.ForeignKey(
        "Guru", on_delete=models.SET_NULL, null=True, blank=True
    )

    # Birth details
    dob = models.DateField(verbose_name=_("Date of birth"), null=True,)
    is_tob_unknown = models.BooleanField(
        choices=BOOL_YES_NO, null=True, verbose_name=_("Is Birth Time unknown?")
    )
    tob = models.TimeField(
        help_text="Enter time HH:MM:SS in 24hr format",
        verbose_name=_("Birth Time"),
        null=True,
        blank=True,
    )
    birth_city = models.CharField(
        max_length=200,
        verbose_name=_("City of birth"),
        help_text="Birth village/town/city (auto populated from map)",
        null=True,
        blank=True,
    )
    birth_state = models.CharField(
        max_length=200,
        verbose_name=_("State of birth"),
        help_text=_("Auto populated from map"),
        null=True,
        blank=True,
    )
    birth_country = models.ForeignKey(
        "Country",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="birthCountry",
        verbose_name=_("Country of birth"),
    )
    birth_place = PlacesField(null=True, blank=True)
    gotra = models.ForeignKey(Gotra, on_delete=models.SET_NULL, blank=True, null=True)

    # Current location details
    current_place = PlacesField(null=True, blank=True)
    current_city = models.CharField(
        max_length=200,
        verbose_name=_("City"),
        help_text="Current village/town/city (auto populated from map)",
        null=True,
        blank=True,
    )
    current_state = models.CharField(
        max_length=200,
        verbose_name=_("State"),
        help_text=_("Auto populated from map"),
        null=True,
        blank=True,
    )
    current_country = models.ForeignKey(
        "Country",
        on_delete=models.SET_NULL,
        null=True,
        related_name="currentCountry",
        verbose_name=_("Country"),
        blank=True,
    )
    nationality = models.ForeignKey(
        Nationality, on_delete=models.SET_NULL, blank=True, null=True,
    )

    # Language details
    mother_tongue = models.ForeignKey(
        "Language", on_delete=models.SET_NULL, null=True, blank=True
    )
    languages_can_speak = models.ManyToManyField(
        "Language", help_text="Languages you know", related_name="speakers", blank=True,
    )
    languages_can_read_write = models.ManyToManyField(
        "Language",
        verbose_name="Languages you can read and write",
        related_name="readers_and_writers",
        blank=True,
    )

    # Physical appearance
    height = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Height in cms",
        null=True,
        blank=True,
    )
    complexion = models.CharField(
        max_length=3,
        help_text="Enter your complexion",
        choices=COMPLEXION_CHOICES,
        null=True,
        blank=True,
    )
    body_type = models.CharField(
        max_length=3, choices=BODY_TYPE, null=True, blank=True,
    )
    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Weight in kgs",
        null=True,
        blank=True,
    )
    color_of_eyes = models.CharField(
        max_length=3, choices=COLOR_OF_EYES, null=True, blank=True,
    )
    hair_color = models.CharField(
        max_length=3, choices=HAIR_COLOR, null=True, blank=True,
    )

    # Personality
    personality = models.TextField(
        max_length=1500, verbose_name="Describe yourself", null=True, blank=True
    )
    recreational_activities = models.CharField(
        max_length=250,
        verbose_name="List your favorite recreational activities",
        null=True,
        blank=True,
    )
    devotional_services = models.CharField(
        max_length=250,
        verbose_name="List your favorite devotional service",
        null=True,
        blank=True,
    )

    # Professional details
    education = models.ManyToManyField(
        "Education", blank=True, help_text="HS, Graduate etc.",
    )
    education_details = models.TextField(
        max_length=100, null=True, verbose_name="Education in Detail", blank=True,
    )
    institution = models.CharField(
        max_length=75,
        blank=True,
        null=True,
        verbose_name="College/Institution",
        help_text="Enter College/Institution Name",
    )
    employed_in = models.CharField(
        max_length=3, null=True, choices=EMPLOYED_IN_CHOICES, blank=True,
    )
    occupations = models.ManyToManyField(
        "Occupation", blank=True, help_text="Doctor, Engineer, Entrepreneur etc.",
    )
    occupation_details = models.TextField(
        max_length=100, null=True, verbose_name="Occupation in Detail", blank=True,
    )
    organization = models.CharField(
        max_length=75, null=True, help_text="Enter Organization Name", blank=True,
    )
    annual_income = MoneyField(
        max_digits=20, decimal_places=2, null=True, default_currency="INR", blank=True
    )
    annual_income_in_base_currency = MoneyField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        default_currency="INR",
        verbose_name=_("Annual income in {}".format(settings.BASE_CURRENCY)),
    )

    # Religion/Caste details
    religion = models.ForeignKey(
        Religion, on_delete=models.SET_NULL, null=True, blank=True
    )
    caste = models.ForeignKey(Caste, on_delete=models.SET_NULL, null=True, blank=True)
    caste_other = models.CharField(
        max_length=50, verbose_name="Other caste", blank=True, default=""
    )
    subcaste = models.ForeignKey(
        Subcaste, on_delete=models.SET_NULL, null=True, blank=True
    )
    subcaste_other = models.CharField(
        max_length=50, verbose_name="Other subcaste", blank=True, default=""
    )

    # Family details
    are_parents_devotees = models.CharField(
        max_length=2,
        choices=ARE_PARENTS_DEV,
        null=True,
        blank=True,
        verbose_name="Are your parents devotees?",
    )
    family_values = models.CharField(
        max_length=4, choices=FAMILY_VALUE_CHOICES, null=True, blank=True,
    )
    family_type = models.CharField(
        max_length=3, choices=FAMILY_TYPE_CHOICES, null=True, blank=True,
    )
    family_status = models.CharField(
        max_length=2, choices=FAMILY_STATUS_CHOICES, null=True, blank=True,
    )
    father_status = models.CharField(
        max_length=3, choices=FATHER_STATUS_CHOICES, null=True, blank=True,
    )
    mother_status = models.CharField(
        max_length=3, choices=MOTHER_STATUS_CHOICES, null=True, blank=True,
    )
    brothers = models.PositiveIntegerField(
        null=True, blank=True, verbose_name="No. of Brothers", default=0
    )
    sisters = models.PositiveIntegerField(
        null=True, blank=True, verbose_name="No. of Sisters", default=0
    )
    brothers_married = models.PositiveIntegerField(null=True, blank=True, default=0)
    sisters_married = models.PositiveIntegerField(null=True, blank=True, default=0)
    family_location = models.CharField(
        max_length=10, choices=FAMILY_LOCATION_CHOICES, null=True, blank=True,
    )
    family_origin = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Ancestral origin or father's birth place",
        verbose_name="Ancestral/Family Origin",
    )
    religious_background = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Religious background of the family",
    )
    family_details = models.TextField(max_length=200, blank=True, null=True,)

    # Medical details
    want_children = models.CharField(
        max_length=2,
        choices=Y_N_MAYB,
        verbose_name="Do you want Children",
        null=True,
        blank=True,
    )
    medical_history = models.TextField(max_length=250, null=True, blank=True)

    matches = models.ManyToManyField(
        "self", through="Match", blank=True, symmetrical=False
    )

    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="matrimony_profile",
    )

    updated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="+",
    )

    # Staff users
    assignee = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_profiles",
    )
    comments = GenericRelation("Comment")

    @property
    def get_languages_can_speak(self):
        if self.languages_can_speak is not None:
            return ", ".join(p.name for p in self.languages_can_speak.all())
        else:
            return None

    @property
    def get_languages_can_read_write(self):
        if self.languages_can_read_write is not None:
            return ", ".join(p.name for p in self.languages_can_read_write.all())
        else:
            return None

    @property
    def education_text(self):
        return ", ".join([item.name for item in self.education.all()])

    @property
    def occupations_text(self):
        return ", ".join([item.name for item in self.occupations.all()])

    @property
    def primary_image(self):
        primary_img = self.get_primary_image_obj()
        if not primary_img:
            return ""
        return format_html(
            '<img src ="{}" style="width:90px; \
            height: 90px"/>'.format(
                primary_img.photo.image.url
            )
        )

    @property
    def primary_image_url(self):
        primary_img = self.get_primary_image_obj()
        if not primary_img:
            return ""
        return primary_img.photo.image.url

    @property
    def primary_image_thumbnail_url(self):
        primary_img = self.get_primary_image_obj()
        if not primary_img:
            return ""
        return primary_img.photo.get_thumbnail_url()

    def get_primary_image_obj(self):
        objs = self.photo_set.filter(primary=True)
        return objs[0] if objs else None

    @property
    def is_registered(self):
        return True if self.user.is_matrimony_registration_complete else False

    @property
    def is_active(self):
        return True if self.status >= "20" else False

    @property
    def age(self):
        if self.dob:
            return int((datetime.datetime.now().date() - self.dob).days / 365.25)

    @property
    def matches(self):
        return (
            self.female_matches.all() if self.gender == "M" else self.male_matches.all()
        )

    def match_profiles(self, response=None):
        query_kwargs = {}
        values_list_fields = ["female__id" if self.gender == "M" else "male__id"]
        matches = None

        if response in ["ACP", "REJ"]:
            query_kwargs[
                "female_response" if self.gender == "M" else "male_response"
            ] = response

        return MatrimonyProfile.objects.filter(
            id__in=self.matches.filter(**query_kwargs).values_list(
                *values_list_fields, flat=True
            )
        )

    @property
    def matching_profiles_list(self):
        matches = []
        if self.gender == "M":
            for m in self.female_matches.all():
                matches.append(
                    (
                        m.id,
                        m.female,
                        m.show_female_photos,
                        m.female_response,
                        m.male_response,
                    )
                )
        else:
            for m in self.male_matches.all():
                matches.append(
                    (
                        m.id,
                        m.male,
                        m.show_male_photos,
                        m.male_response,
                        m.female_response,
                    )
                )
        return matches

    @property
    def mentor(self):
        return self.mentors.all()[0] if self.mentors.all() else None

    @property
    def expectations(self):
        return self.expectations.all()[0]

    @property
    def matching_profiles_url(self):
        from urllib.parse import urlencode, quote_plus

        querystr = urlencode({"q-l": "on", "q": self.expectations.djangoql_query_str})
        return "{}matrimony/{}/?{}".format(
            reverse("admin:index"), "female" if self.gender == "M" else "male", querystr
        )

    def search_profiles(self, querydata=None):
        """
        When querydata is None, return preferred profiles as per expectations, by default.
        """
        MARITAL_STATUS_DICT = dict(MARITAL_STATUS)
        EMPLOYED_IN_CHOICES_DICT = dict(EMPLOYED_IN_CHOICES)
        SPIRITUAL_STATUS_CHOICES_DICT = dict(SPIRITUAL_STATUS_CHOICES)

        if self.gender == "M":
            q = Q(gender="F")
        else:
            q = Q(gender="M")

        age_from = (
            querydata.get("age_from") if querydata else self.expectations.age_from
        )
        if age_from:
            q = q & Q(
                dob__lte=(timezone.datetime.now() - relativedelta(years=age_from))
            )

        age_to = querydata.get("age_to") if querydata else self.expectations.age_to
        if age_to:
            q = q & Q(dob__gte=(timezone.datetime.now() - relativedelta(years=age_to)))

        height_from = (
            querydata.get("height_from") if querydata else self.expectations.height_from
        )
        if height_from:
            q = q & Q(height__gte=height_from)

        height_to = (
            querydata.get("height_to") if querydata else self.expectations.height_to
        )
        if height_to:
            q = q & Q(height__lte=height_to)

        religions = (
            querydata.get("religions")
            if querydata
            else self.expectations.religions.all()
        )
        if religions:
            q = q & Q(religion__name__in=[f"{r.name}" for r in religions])

        mother_tongues = (
            querydata.get("mother_tongues")
            if querydata
            else self.expectations.mother_tongues.all()
        )
        if mother_tongues:
            q = q & Q(mother_tongue__name__in=[f"{l.name}" for l in mother_tongues])

        castes = (
            querydata.get("castes") if querydata else self.expectations.castes.all()
        )
        if castes:
            q = q & Q(caste__name__in=[f"{c.name}" for c in castes])

        subcastes = (
            querydata.get("subcastes")
            if querydata
            else self.expectations.subcastes.all()
        )
        if subcastes:
            q = q & Q(subcaste__name__in=[f"{sc.name}" for sc in subcastes])

        countries_living_in = (
            querydata.get("countries_living_in")
            if querydata
            else self.expectations.countries_living_in.all()
        )
        if countries_living_in:
            q = q & Q(current_country__in=countries_living_in)

        ethnicities = (
            querydata.get("ethnicities")
            if querydata
            else self.expectations.ethnicities.all()
        )
        if ethnicities:
            q = q & Q(ethnic_origin__in=ethnicities)

        marital_status = (
            querydata.get("marital_status")
            if querydata
            else self.expectations.marital_status
        )
        if marital_status:
            q = q & Q(marital_status__in=marital_status)

        want_nri = (
            querydata.get("want_nri") if querydata else self.expectations.want_nri
        )
        if want_nri == "Y":
            q = q & ~Q(current_country__name="India")
        elif want_nri == "N":
            q = q & Q(current_country__name="India")

        languages_can_speak = (
            querydata.get("languages_can_speak")
            if querydata
            else self.expectations.languages_can_speak.all()
        )
        if languages_can_speak:
            q = q & Q(languages_can_speak__in=languages_can_speak)

        languages_can_read_write = (
            querydata.get("languages_can_read_write")
            if querydata
            else self.expectations.languages_can_read_write.all()
        )
        if languages_can_read_write:
            q = q & Q(languages_can_read_write__in=languages_can_read_write)

        education = (
            querydata.get("education")
            if querydata
            else self.expectations.education.all()
        )
        if education:
            q = q & Q(education__in=education)

        occupations = (
            querydata.get("occupations")
            if querydata
            else self.expectations.occupations.all()
        )
        if occupations:
            q = q & Q(occupations__in=occupations)

        employed_in = (
            querydata.get("employed_in") if querydata else self.expectations.employed_in
        )
        if employed_in:
            q = q & Q(employed_in__in=employed_in)

        spiritual_status = (
            querydata.get("spiritual_status")
            if querydata
            else self.expectations.spiritual_status
        )
        if spiritual_status:
            q = q & Q(spiritual_status__in=spiritual_status)

        annual_income_from = (
            querydata.get("annual_income_from")
            if querydata
            else self.expectations.annual_income_from
        )
        if annual_income_from:
            q = q & Q(
                annual_income_in_base_currency__gte=convert_money(
                    annual_income_from, settings.BASE_CURRENCY
                ).amount
            )

        annual_income_to = (
            querydata.get("annual_income_to")
            if querydata
            else self.expectations.annual_income_to
        )
        if annual_income_to:
            q = q & Q(
                annual_income_in_base_currency__lte=convert_money(
                    annual_income_to, settings.BASE_CURRENCY
                ).amount
            )

        spiritual_masters = (
            querydata.get("spiritual_masters")
            if querydata
            else self.expectations.spiritual_masters.all()
        )
        if spiritual_masters:
            q = q & Q(
                spiritual_master__name__in=[f"{sm.name}" for sm in spiritual_masters]
            )

        return MatrimonyProfile.objects.filter(q).distinct()

    def is_personal_data_visible_to_user(self, user):
        if user.is_staff or self.match_profiles(response="ACP").filter(user=user):
            return True
        return False

    def __str__(self):
        return self.name

    class Meta:
        db_table = "matrimony_profiles"

        ordering = ["-registration_date"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_annual_income = self.annual_income
        self._original_status = self.status
        self._original_updated_by = self.updated_by

    def set_status(self, status_text):
        d = {v: k for k, v in PROFILE_STATUS_CHOICES}
        self.status = d.get(status_text)

    def add_count(self, initial=False):
        properties = {"gender": "male" if self.gender == "M" else "female"}
        if self.updated_by:
            properties["updated_by"] = self.updated_by.username
        if initial:
            count(
                self.profile_id,
                "profile-{}".format(
                    "-".join(PROFILE_STATUS_CHOICES_DICT["00"].lower().split())
                ),
                properties,
            )
            if self.status == "00":
                return
        count(
            self.profile_id,
            "profile-{}".format(
                "-".join(PROFILE_STATUS_CHOICES_DICT[self.status].lower().split())
            ),
            properties,
        )

    def save(self, *args, **kwargs):
        create = False
        if self.id is None:
            self.profile_id = self.generate_profile_id()
            create = True
        if self.annual_income and (
            self.id is None or self._original_annual_income != self.annual_income
        ):
            self.annual_income_in_base_currency = convert_money(
                self.annual_income, settings.BASE_CURRENCY
            )

        super().save(*args, **kwargs)

        if self._original_status != self.status or create:
            self.add_count()
        _, created = MatrimonyProfileStats.objects.get_or_create(profile=self)
        _, created = Expectation.objects.get_or_create(profile=self)

    def send_batch_matches_email(self):
        body = self.get_batch_matches_email_body()
        subject = _("Matches for you")
        mail.send(
            self.email,
            subject=_("Suggested matches"),
            html_message=body,
            headers={"Reply-to": settings.EMAIL_CONTACT},
            priority="medium",
        )

    def get_batch_matches_email_body(self):
        return loader.get_template("matrimony/emails/matches.html").render(
            {"matches": self.matching_profiles_list}
        )

    def generate_profile_id(self):
        digest = (
            md5(
                f"{self.name}-{self.gender}-{self.phone}-{self.email}-{self.dob}-{self.phone}".encode(
                    "utf-8"
                )
            )
            .hexdigest()[:7]
            .upper()
        )
        return f"{settings.PROFILE_ID_PREFIX}{digest}"

    def update_stats(self):
        _, created = MatrimonyProfileStats.objects.get_or_create(profile=self)
        matches_suggested = (
            matches_accepted
        ) = matches_rejected = matches_accepted_by = matches_rejected_by = 0
        self_response_field_name = (
            "male_response" if self.gender == "M" else "female_response"
        )
        response_field_name = (
            "female_response" if self.gender == "M" else "male_response"
        )
        for m in self.matches:
            matches_suggested += 1
            matches_accepted += (
                1 if getattr(m, self_response_field_name) == "ACP" else 0
            )
            matches_rejected += (
                1 if getattr(m, self_response_field_name) == "REJ" else 0
            )
            matches_accepted_by += 1 if getattr(m, response_field_name) == "ACP" else 0
            matches_rejected_by += 1 if getattr(m, response_field_name) == "REJ" else 0
        self.stats.matches_suggested = matches_suggested
        self.stats.matches_accepted = matches_accepted
        self.stats.matches_rejected = matches_rejected
        self.stats.matches_accepted_by = matches_accepted_by
        self.stats.matches_rejected_by = matches_rejected_by
        self.stats.save()

    def create_user(self):
        user, created = User.objects.get_or_create(
            username=self.profile_id, email=self.email, is_matrimony_candidate=True,
        )
        if created:
            self.user = user
            self.save()
            self.send_profile_import_email()
            user.send_confirmation_email()

        if self.name != user.name:
            user.name = self.name
            user.save()

        return user

    def send_profile_import_email(self):
        site = Site.objects.get_current()
        msg = loader.get_template("matrimony/emails/profile_import.txt").render(
            {
                "current_site": site,
                "password_reset_link": build_absolute_url(
                    reverse("account_reset_password")
                ),
                "contact_email": settings.EMAIL_CONTACT,
            }
        )
        mail.send(
            self.email,
            subject=_("Matrimony profile created"),
            html_message=msg,
            headers={"Reply-to": settings.EMAIL_CONTACT},
            priority="medium",
        )


class Expectation(BaseModel):
    profile = models.OneToOneField(
        MatrimonyProfile,
        related_name="expectations",
        unique=True,
        on_delete=models.CASCADE,
    )

    # Basic preferences
    age_from = models.PositiveIntegerField(
        null=True, blank=True, verbose_name="From age"
    )
    age_to = models.PositiveIntegerField(null=True, blank=True, verbose_name="To age")
    height_from = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="From height",
    )
    height_to = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="To height"
    )
    marital_status = MultiSelectField(
        choices=MARITAL_STATUS, max_choices=10, max_length=100, null=True, blank=True
    )

    # Religuous preferences
    religions = models.ManyToManyField(Religion, blank=True,)
    mother_tongues = models.ManyToManyField(Language, blank=True)
    castes = models.ManyToManyField(Caste, blank=True)
    subcastes = models.ManyToManyField(Subcaste, blank=True)

    # Location preferences
    countries_living_in = models.ManyToManyField(Country, blank=True)
    nationalities = models.ManyToManyField(
        Nationality, related_name="nationalities", blank=True
    )
    ethnicities = models.ManyToManyField(
        Nationality, related_name="ethnicities", blank=True
    )
    want_nri = models.CharField(
        max_length=2,
        choices=Y_N_MAYB,
        verbose_name="Do you want NRI",
        null=True,
        blank=True,
    )

    # Language preferences
    languages_can_speak = models.ManyToManyField(
        "Language",
        help_text="Languages the spouse should know to speak",
        related_name="languages_spouse_know",
        blank=True,
    )
    languages_can_read_write = models.ManyToManyField(
        "Language",
        verbose_name="Languages the spouse should know to read and write",
        related_name="languages_spouse_read_write",
        blank=True,
    )

    # Professional preferences
    education = models.ManyToManyField(Education, blank=True)
    occupations = models.ManyToManyField(Occupation, blank=True)
    employed_in = MultiSelectField(
        choices=EMPLOYED_IN_CHOICES,
        max_choices=10,
        max_length=100,
        null=True,
        blank=True,
    )
    annual_income_from = MoneyField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        default_currency="INR",
        verbose_name="From annual income",
    )
    annual_income_from_in_base_currency = MoneyField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        default_currency="INR",
        verbose_name="From annual income ({})".format(settings.BASE_CURRENCY),
    )
    annual_income_to = MoneyField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        default_currency="INR",
        verbose_name="To annual income",
    )
    annual_income_to_in_base_currency = MoneyField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        default_currency="INR",
        verbose_name="To annual income ({})".format(settings.BASE_CURRENCY),
    )

    # Spiritual details
    spiritual_status = MultiSelectField(
        choices=SPIRITUAL_STATUS_CHOICES,
        max_choices=10,
        max_length=50,
        null=True,
        blank=True,
    )
    spiritual_masters = models.ManyToManyField(Guru, blank=True,)
    min_rounds_chanting = models.PositiveIntegerField(
        null=True, blank=True, verbose_name="Minimum rounds of japa",
    )

    partner_description = models.TextField(max_length=1500, null=True, blank=True)

    class Meta:
        db_table = "matrimony_expectations"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_annual_income_from = self.annual_income_from
        self._original_annual_income_to = self.annual_income_to

    def save(self, *args, **kwargs):
        if self.annual_income_from and (
            self.id is None
            or self._original_annual_income_from != self.annual_income_from
        ):
            self.annual_income_from_in_base_currency = convert_money(
                self.annual_income_from, settings.BASE_CURRENCY
            )
        if self.annual_income_to and (
            self.id is None or self._original_annual_income_to != self.annual_income_to
        ):
            self.annual_income_to_in_base_currency = convert_money(
                self.annual_income_to, settings.BASE_CURRENCY
            )
        return super().save(*args, **kwargs)

    @property
    def djangoql_query_str(self):
        MARITAL_STATUS_DICT = dict(MARITAL_STATUS)
        EMPLOYED_IN_CHOICES_DICT = dict(EMPLOYED_IN_CHOICES)
        SPIRITUAL_STATUS_CHOICES_DICT = dict(SPIRITUAL_STATUS_CHOICES)
        query = []
        if self.age_from:
            query.append(
                'dob <= "{}"'.format(
                    (
                        timezone.datetime.now() - relativedelta(years=self.age_from)
                    ).strftime("%Y-%m-%d")
                )
            )
        if self.age_to:
            query.append(
                'dob >= "{}"'.format(
                    (
                        timezone.datetime.now() - relativedelta(years=self.age_to)
                    ).strftime("%Y-%m-%d")
                )
            )
        if self.height_from:
            query.append(f"height >= {self.height_from}")
        if self.height_to:
            query.append(f"height <= {self.height_to}")
        if self.religions.all():
            query.append(
                "religion.name in ({})".format(
                    ",".join([f'"{r.name}"' for r in self.religions.all()])
                )
            )
        if self.mother_tongues.all():
            query.append(
                "mother_tongue.name in ({})".format(
                    ",".join([f'"{l.name}"' for l in self.mother_tongues.all()])
                )
            )
        if self.castes.all():
            query.append(
                "caste.name in ({})".format(
                    ",".join([f'"{c.name}"' for c in self.castes.all()])
                )
            )
        if self.subcastes.all():
            query.append(
                "subcaste.name in ({})".format(
                    ",".join([f'"{sc.name}"' for sc in self.subcastes.all()])
                )
            )
        if self.marital_status:
            query.append(
                "marital_status in ({})".format(
                    ",".join(
                        [f'"{MARITAL_STATUS_DICT[ms]}"' for ms in self.marital_status]
                    )
                )
            )
        if self.employed_in:
            query.append(
                "employed_in in ({})".format(
                    ",".join(
                        [f'"{EMPLOYED_IN_CHOICES_DICT[ei]}"' for ei in self.employed_in]
                    )
                )
            )
        if self.spiritual_status:
            query.append(
                "spiritual_status in ({})".format(
                    ",".join(
                        [
                            f'"{SPIRITUAL_STATUS_CHOICES_DICT[ss]}"'
                            for ss in self.spiritual_status
                        ]
                    )
                )
            )
        if self.annual_income_from:
            query.append(
                f"annual_income_in_base_currency >= {self.annual_income_from_in_base_currency.amount}"
            )
        if self.annual_income_to:
            query.append(
                f"annual_income_in_base_currency <= {self.annual_income_to_in_base_currency.amount}"
            )
        if self.spiritual_masters.all():
            query.append(
                "spiritual_master.name in ({})".format(
                    ",".join([f'"{sm.name}"' for sm in self.spiritual_masters.all()])
                )
            )
        # FIXME: implement query for NRI

        return " and ".join(query)

    @property
    def religions_text(self):
        return ", ".join([item.name for item in self.religions.all()])

    @property
    def mother_tongues_text(self):
        return ", ".join([item.name for item in self.mother_tongues.all()])

    @property
    def castes_text(self):
        return ", ".join([item.name for item in self.castes.all()])

    @property
    def subcastes_text(self):
        return ", ".join([item.name for item in self.subcastes.all()])

    @property
    def countries_living_in_text(self):
        return ", ".join([item.name for item in self.countries_living_in.all()])

    @property
    def ethnicities_text(self):
        return ", ".join([item.name for item in self.ethnicities.all()])

    @property
    def languages_can_speak_text(self):
        return ", ".join([item.name for item in self.languages_can_speak.all()])

    @property
    def languages_can_read_write_text(self):
        return ", ".join([item.name for item in self.languages_can_read_write.all()])

    @property
    def education_text(self):
        return ", ".join([item.name for item in self.education.all()])

    @property
    def occupations_text(self):
        return ", ".join([item.name for item in self.occupations.all()])

    @property
    def spiritual_masters_text(self):
        return ", ".join([item.name for item in self.spiritual_masters.all()])


class MaleManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(gender="M")


class Male(MatrimonyProfile):
    objects = money_manager(MaleManager())

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if self.id is None:
            self.gender = "M"
        super().save(*args, **kwargs)


class FemaleManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(gender="F")


class Female(MatrimonyProfile):
    objects = money_manager(FemaleManager())

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if self.id is None:
            self.gender = "F"
        super().save(*args, **kwargs)


MATCH_RESPONSE_CHOICES = (("", _("")), ("ACP", _("Accepted")), ("REJ", _("Rejected")))
MATCH_STATUS_CHOICES = (
    ("", _("")),
    ("SUG", _("Suggested")),
    ("SNT", _("Sent")),
    ("TON", _("To notify")),
    ("NTF", _("Notified")),
    ("ACP", _("Accepted")),
    ("REJ", _("Rejected")),
    ("FOL", _("Follow up")),
    ("PRD", _("Parties discussing")),
    ("MRC", _("Marriage cancelled")),
    ("MRF", _("Marriage finalized")),
    ("MRD", _("Married")),
)

MATCH_CATEGORY_CHOICES = (
    ("USR", _("User")),
    ("STF", _("Staff")),
    ("SYS", _("Auto generated")),
)

class Match(BaseModel):
    category = models.CharField(
        max_length=3, choices=MATCH_CATEGORY_CHOICES, blank=True, default="STF"
    )
    is_mutual = models.NullBooleanField(blank=True, help_text="Is it a mutual match based on expectations?")
    is_visible = models.NullBooleanField(blank=True, help_text="Is match visible to users?")
    show_personal_info = models.NullBooleanField(blank=True, default=False, help_text="Show personal profile info")
    notified = models.NullBooleanField(blank=True)

    male = models.ForeignKey(
        Male,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="female_matches",
    )

    male_response = models.CharField(
        max_length=3, choices=MATCH_RESPONSE_CHOICES, blank=True, default=""
    )
    male_photos_visibility = models.NullBooleanField(blank=True)
    male_response_updated_at = models.DateTimeField(blank=True, null=True)

    female = models.ForeignKey(
        Female,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="male_matches",
    )
    female_response = models.CharField(
        max_length=3, choices=MATCH_RESPONSE_CHOICES, blank=True, default=""
    )
    female_photos_visibility = models.NullBooleanField(blank=True)
    female_response_updated_at = models.DateTimeField(blank=True, null=True)

    sender_gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)

    status = models.CharField(
        max_length=3, choices=MATCH_STATUS_CHOICES, blank=True, default=""
    )
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    comments = GenericRelation("Comment")

    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="+",
    )
    updated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="+",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_male_response = self.male_response
        self._original_female_response = self.female_response

    def __str__(self):
        return f"{self.male}/{self.female}"

    @property
    def response(self):
        return "Accepted" if self.male_response == self.female_response == "ACP" else "Rejected"

    class Meta:
        db_table = "matrimony_matches"

        indexes = [
            models.Index(fields=["male"]),
            models.Index(fields=["female"]),
        ]

        unique_together = [["male", "female"]]

        verbose_name = "Match"
        verbose_name_plural = "Matches"

    @property
    def show_male_photos(self):
        if self.male_photos_visibility is not None:
            return (
                self.male.photos_visible_to_all_matches and self.male_photos_visibility
            )
        return self.male.photos_visible_to_all_matches or self.male_response == "ACP"

    @property
    def show_female_photos(self):
        if self.female_photos_visibility is not None:
            return (
                self.female.photos_visible_to_all_matches
                and self.female_photos_visibility
            )
        return (
            self.female.photos_visible_to_all_matches or self.female_response == "ACP"
        )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if (
            self._original_male_response != self.male_response
            or self._original_female_response != self.female_response
        ):
            self.male.update_stats()
            self.female.update_stats()


class Photo(BaseModel):
    profile = models.ForeignKey(MatrimonyProfile, on_delete=models.CASCADE)
    photo = models.ForeignKey(
        "photologue.Photo", on_delete=models.CASCADE, related_name="photo_set"
    )

    primary = models.BooleanField(default=False, blank=True)

    @property
    def thumbnail(self):
        from django.utils.html import mark_safe

        if not self.photo:
            return ""
        return mark_safe(
            f"""
<a href="{self.photo.image.url}">
    <img src="{self.photo.get_thumbnail_url()}" alt="{self.photo.title}">
</a>"""
        )

    class Meta:
        db_table = "matrimony_photos"
        indexes = [
            models.Index(fields=["profile"]),
        ]

    def save(self, *args, **kwargs):
        if self.primary:
            try:
                temp = Photo.objects.get(primary=True, profile=self.profile)
                if self != temp:
                    temp.primary = False
                    temp.save()
            except Photo.DoesNotExist:
                pass
        super().save(*args, **kwargs)


class Comment(BaseModel):
    message = models.TextField(max_length=2000, default="")
    timestamp = models.DateTimeField(default=timezone.now, blank=True)
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="+",
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        db_table = "comments"
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]


class Mentor(BaseModel):
    """Model representing Mentors or Spirtual References/Counsellors for users"""

    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=17, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    profile = models.ForeignKey(
        MatrimonyProfile, on_delete=models.CASCADE, related_name="mentors", null=True
    )

    class Meta:
        ordering = ["name"]
        db_table = "mentor"
        unique_together = ("name", "profile")

    def __str__(self):
        return f"{self.name}"


class MatrimonyProfileStats(BaseModel):
    profile = models.OneToOneField(
        MatrimonyProfile, unique=True, related_name="stats", on_delete=models.CASCADE
    )
    matches_suggested = models.PositiveIntegerField(default=0, blank=True, null=True)
    matches_accepted = models.PositiveIntegerField(default=0, blank=True, null=True)
    matches_rejected = models.PositiveIntegerField(default=0, blank=True, null=True)
    matches_accepted_by = models.PositiveIntegerField(default=0, blank=True, null=True)
    matches_rejected_by = models.PositiveIntegerField(default=0, blank=True, null=True)

    class Meta:
        db_table = "matrimony_profile_stats"
