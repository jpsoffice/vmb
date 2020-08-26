import datetime
from hashlib import md5

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.template import loader, Context
from django.utils.html import format_html
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from djmoney.contrib.exchange.models import convert_money
from places.fields import PlacesField

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
PROFILE_STATUS_CHOICES = (
    ("00", "New"),
    ("01", "Acknowledged"),
    ("02", "Awaiting response"),
    ("03", "Inactive"),
    ("04", "Blocked"),
    ("10", "Active"),
    ("11", "Backlog"),
    ("12", "In progress"),
    ("13", "On hold"),
    ("20", "Married (outside sources)"),
    ("30", "Married"),
)
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
    ("Mb", "May be"),
)
CHILDREN_COUNT = (
    (0, "0"),
    (1, "1"),
    (2, "2"),
    (3, "3"),
)


class MatrimonyProfile(BaseModel):
    """Model representing matrimonial profile of a candidate"""

    profile_id = models.CharField(max_length=15, blank=True, unique=True)
    name = models.CharField(max_length=200, verbose_name=_("Name"),)
    spiritual_name = models.CharField(
        max_length=200, default="", blank=True, verbose_name=_("Spiritual name")
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

    images = models.ManyToManyField("photologue.Photo", through="Image", blank=True)

    # Contact details
    email = models.EmailField(null=True, verbose_name=_("Email"))
    phone = models.CharField(max_length=17, verbose_name=_("Phone number"), null=True,)

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
    dob = models.DateField(
        help_text="Enter birth date as YYYY-MM-DD",
        verbose_name=_("date of birth"),
        null=True,
    )
    tob = models.TimeField(
        help_text="Enter time HH:MM:SS in 24hr format",
        verbose_name=_("Birth Time"),
        null=True,
        blank=True,
    )
    birth_city = models.CharField(
        max_length=200,
        verbose_name=_("City"),
        help_text="Enter birth village/town/city",
        null=True,
        blank=True,
    )
    birth_state = models.CharField(
        max_length=200, verbose_name=_("State"), null=True, blank=True
    )
    birth_country = models.ForeignKey(
        "Country",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="birthCountry",
        verbose_name=_("Country"),
    )
    birth_place = PlacesField(null=True, blank=True)
    gotra = models.ForeignKey(Gotra, on_delete=models.SET_NULL, blank=True, null=True)

    # Current location details
    current_place = PlacesField(null=True, blank=True)
    current_city = models.CharField(
        max_length=200,
        verbose_name=_("City"),
        help_text="Enter current village/town/city",
        null=True,
        blank=True,
    )
    current_state = models.CharField(
        max_length=200, verbose_name=_("State"), null=True, blank=True,
    )
    current_country = models.ForeignKey(
        "Country",
        on_delete=models.SET_NULL,
        null=True,
        related_name="currentCountry",
        verbose_name=_("Country"),
        blank=True,
    )
    nationality = models.ForeignKey(Nationality, on_delete=models.SET_NULL, null=True,)

    # Language details
    mother_tongue = models.ForeignKey(
        "Language", on_delete=models.SET_NULL, null=True, blank=True
    )
    languages_known = models.ManyToManyField(
        "Language",
        help_text="Languages you know",
        related_name="languages_known",
        blank=True,
    )
    languages_read_write = models.ManyToManyField(
        "Language",
        verbose_name="Languages you can read and write",
        related_name="languages_read_write",
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
    subcaste = models.ForeignKey(
        Subcaste, on_delete=models.SET_NULL, null=True, blank=True
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

    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="+"
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
    def get_languages_known(self):
        if self.languages_known is not None:
            return ", ".join(p.name for p in self.languages_known.all())
        else:
            return None

    @property
    def get_languages_read_write(self):
        if self.languages_read_write is not None:
            return ", ".join(p.name for p in self.languages_read_write.all())
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
        if self.images is not None and self.images != "":
            return format_html(
                '<img src ="{}" style="width:90px; \
                height: 90px"/>'.format(
                    Image.objects.get(profile=self, primary=True).photo.image.url
                )
            )

    @property
    def primary_image_url(self):
        try:
            return Image.objects.get(profile=self, primary=True).photo.image.url
        except Image.DoesNotExist:
            return ""

    @property
    def primary_image_thumbnail_url(self):
        try:
            return Image.objects.get(
                profile=self, primary=True
            ).photo.get_thumbnail_url()
        except Image.DoesNotExist:
            return ""

    @property
    def age(self):
        if self.dob:
            return int((datetime.datetime.now().date() - self.dob).days / 365.25)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "matrimony_profiles"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_annual_income = self.annual_income
        self._original_birth_place = self.birth_place
        self._original_current_place = self.current_place

    def save(self, *args, **kwargs):
        if self.annual_income and (
            self.id is None or self._original_annual_income != self.annual_income
        ):
            self.annual_income_in_base_currency = convert_money(
                self.annual_income, settings.BASE_CURRENCY
            )

        if self.id is None or self._original_birth_place != self.birth_place:
            if self.birth_place:
                (
                    self.birth_city,
                    self.birth_state,
                    country,
                ) = self.birth_place.place.split(", ")[-3:]
                countries = Country.objects.filter(Q(name=country) | Q(code=country))
                self.birth_country = countries[0] if countries else None
            else:
                self.birth_city = self.birth_state = self.birth_country = None

        if self.id is None or self._original_current_place != self.current_place:
            if self.current_place:
                (
                    self.current_city,
                    self.current_state,
                    current_country,
                ) = self.current_place.place.split(", ")[-3:]
                countries = Country.objects.filter(
                    Q(name=current_country) | Q(code=current_country)
                )
                self.current_country = countries[0] if countries else None
            else:
                self.current_city = self.current_state = self.current_country = None

        return super().save(*args, **kwargs)

    def send_batch_matches_email(self):
        body = self.get_batch_matches_email_body()
        subject = _("Matches for you")
        email_message = self.email_messages.create(
            sender=settings.MATRIMONY_SENDER_EMAIL,
            subject="Suggested matches",
            body=body,
            to=self.email,
            category="DMD",
            status="NEW",
        )
        email_message.send()

    def get_batch_matches_email_body(self):
        matches = []
        if self.gender == "M":
            for m in self.female_matches.all():
                matches.append(m.female)
        else:
            for m in self.male_matches.all():
                matches.append(m.male)
        return loader.get_template("matrimony/emails/matches.html").render(
            {"matches": matches}
        )

    def generate_profile_id(self):
        digest = (
            md5(
                f"{self.name}-{self.gender}-{self.phone}-{self.email}-{self.dob}-{self.tob}-{self.birth_city}-{self.birth_state}-{self.birth_country}".encode(
                    "utf-8"
                )
            )
            .hexdigest()[:7]
            .upper()
        )
        return f"{settings.PROFILE_ID_PREFIX}{digest}"


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
        choices=MARITAL_STATUS, max_length=100, null=True, blank=True
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
        choices=EMPLOYED_IN_CHOICES, max_length=100, null=True, blank=True
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
        choices=SPIRITUAL_STATUS_CHOICES, max_length=5, null=True, blank=True
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
            self.profile_id = self.generate_profile_id()
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
            self.profile_id = self.generate_profile_id()
        super().save(*args, **kwargs)


MATCH_RESPONSE_CHOICES = (("", _("")), ("ACP", _("Accepted")), ("REJ", _("Rejected")))
MATCH_STATUS_CHOICES = (
    ("", _("")),
    ("SUG", _("Suggested")),
    ("TON", _("To notify")),
    ("NTF", _("Notified")),
    ("FOL", _("Follow up")),
    ("PRD", _("Parties discussing")),
    ("MRC", _("Marriage cancelled")),
    ("MRF", _("Marriage finalized")),
    ("MRD", _("Married")),
)


class Match(BaseModel):
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
    male_response_updated_at = models.DateTimeField(auto_now=True, blank=True)

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
    female_response_updated_at = models.DateTimeField(auto_now=True, blank=True)

    status = models.CharField(
        max_length=3, choices=MATCH_STATUS_CHOICES, blank=True, default=""
    )
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    comments = GenericRelation("Comment")

    def __str__(self):
        return f"{self.male}/{self.female}"

    class Meta:
        db_table = "matrimony_matches"

        verbose_name = "Matche"
        verbose_name_plural = "Matches"


EMAIL_MESSAGE_STATUS_CHOICES = (
    ("NEW", _("New")),
    ("SNT", _("Sent")),
    ("FLD", _("Failed")),
)

EMAIL_MESSAGE_CATEGORY_CHOICES = (
    ("DMD", _("Daily matches digest")),
    ("MAN", _("Manual")),
)


class EmailMessage(BaseModel):
    profile = models.ForeignKey(
        MatrimonyProfile,
        related_name="email_messages",
        on_delete=models.SET_NULL,
        null=True,
    )
    sender = models.EmailField()
    subject = models.CharField(max_length=100)
    body = models.TextField(max_length=2000)
    to = models.EmailField()
    status = models.CharField(
        max_length=3, choices=EMAIL_MESSAGE_STATUS_CHOICES, default="NEW"
    )
    category = models.CharField(
        max_length=3, choices=EMAIL_MESSAGE_CATEGORY_CHOICES, default="MAN"
    )
    sent_at = models.DateTimeField(default=None, null=True, blank=True)

    def send(self):
        from vmb.matrimony.tasks import send_email

        send_email.apply_async(args=[self.id])

    class Meta:
        db_table = "matrimony_email_messages"


class Image(BaseModel):
    profile = models.ForeignKey(MatrimonyProfile, on_delete=models.CASCADE)
    photo = models.ForeignKey(
        "photologue.Photo", on_delete=models.CASCADE, related_name="+"
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
        db_table = "matrimony_images"


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
