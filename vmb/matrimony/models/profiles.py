import datetime
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template import loader, Context
from vmb.users.models import User
from djmoney.models.fields import MoneyField
from djmoney.models.managers import money_manager

from .base import BaseModel
from .relations import Occupation, Qualification, Guru, Language, Country

GENDER_CHOICES = (("M", "Male"), ("F", "Female"), ("O", "Others"))

SPIRITUAL_STATUS_CHOICES = (
    ("A", "Aspiring"),
    ("S", "Shelter"),
    ("D1", "Harinam"),
    ("D2", "Brahmin"),
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
    ("ENG", "Engaged"),
    ("SEP", "Separated"),
    ("DIV", "Divorced"),
    ("WID", "Widowed"),
)

WANT_CHILDREN = (
    ("Y", "Yes"),
    ("N", "No"),
)


class MatrimonyProfile(BaseModel):
    """Model representing matrimonial profile of a candidate"""

    name = models.CharField(max_length=200, verbose_name=_("Name"),)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,)

    images = models.ManyToManyField("photologue.Photo", through="Image", blank=True)

    # Spiritual details
    rounds_chanting = models.IntegerField(
        verbose_name=_("Rounds"),
        help_text="How many rounds are you chanting?",
        default=0,
    )
    spiritual_status = models.CharField(
        max_length=2,
        help_text="Enter spiritual status (e.g. Aspiring, Shelter etc.)",
        choices=SPIRITUAL_STATUS_CHOICES,
        verbose_name=_("Siksha Status"),
        blank=True,
    )
    guru = models.ForeignKey("Guru", on_delete=models.SET_NULL, null=True, blank=True)

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
    )
    birth_city = models.CharField(
        max_length=200,
        verbose_name=_("City"),
        help_text="Enter birth village/town/city",
        null=True,
    )
    birth_state = models.CharField(max_length=200, verbose_name=_("State"), null=True)
    birth_country = models.ForeignKey(
        "Country",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="birthCountry",
        verbose_name=_("Country"),
    )

    # Current location details
    current_city = models.CharField(
        max_length=200,
        verbose_name=_("City"),
        help_text="Enter current village/town/city",
        null=True,
    )
    current_state = models.CharField(
        max_length=200, verbose_name=_("State"), null=True,
    )
    current_country = models.ForeignKey(
        "Country",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="currentCountry",
        verbose_name=_("Country"),
    )

    # Personal details
    languages_known = models.ManyToManyField(
        "Language", help_text="Languages you know", related_name="languages_known",
    )
    languages_read_write = models.ManyToManyField(
        "Language",
        verbose_name="Languages known to read and write",
        related_name="languages_read_write",
    )
    height = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Height in cms",
        blank=True,
        null=True,
    )
    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Weight in kgs",
        blank=True,
        null=True,
    )
    complexion = models.CharField(
        max_length=3,
        help_text="Enter your complexion",
        choices=COMPLEXION_CHOICES,
        blank=True,
        null=True,
    )
    qualification = models.ForeignKey(
        "Qualification",
        on_delete=models.SET_NULL,
        null=True,
        help_text="H.S., Graduate etc.",
    )
    occupation = models.ForeignKey(
        "Occupation",
        on_delete=models.SET_NULL,
        null=True,
        help_text="Surgeon, Computer Application Engineer, etc.",
    )
    annual_income = MoneyField(
        max_digits=10, decimal_places=2, null=True, default_currency="INR"
    )
    marital_status = models.CharField(
        max_length=3,
        choices=MARITAL_STATUS,
        help_text="Single, Divorced etc.",
        null=True,
    )
    recreational_activities = models.CharField(
        max_length=250,
        verbose_name="List your favorite recreational activities",
        blank=True,
        null=True,
    )
    devotional_services = models.CharField(
        max_length=250,
        verbose_name="List your favorite devotional service",
        blank=True,
        null=True,
    )
    personality = models.CharField(
        max_length=250, verbose_name="Describe your personality", blank=True, null=True,
    )

    # Mentors and their details
    mentor1 = models.CharField(
        max_length=250,
        verbose_name="Reference 1",
        help_text="Name, email and mobile number of your Spiritual Mentor/Counsellor 1",
        blank=True,
        null=True,
    )
    mentor2 = models.CharField(
        max_length=250,
        verbose_name="Reference 2",
        help_text="Name, email and mobile number of your Spiritual Mentor/Counsellor 2",
        blank=True,
        null=True,
    )
    children = models.CharField(
        max_length=1,
        choices=WANT_CHILDREN,
        verbose_name="Do you want Children",
        blank=True,
        null=True,
    )
    medical_history = models.CharField(max_length=250, blank=True, null=True,)

    # Family Details
    religion = models.CharField(
        max_length=100,
        verbose_name="Religious Background of family",
        blank=True,
        null=True,
    )
    family_details = models.CharField(max_length=250, blank=True, null=True,)

    # Contact details
    email = models.EmailField(blank=True, null=True, verbose_name=_("Email"))
    phone = models.CharField(max_length=17, verbose_name=_("Phone number"), null=True,)

    expectations = models.TextField(max_length=300, null=True)

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

    @property
    def age(self):
        if self.dob:
            return int((datetime.datetime.now().date() - self.dob).days / 365.25)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "matrimony_profiles"

    def send_batch_matches_email(self):
        body = self.get_batch_matches_email_body()
        subject = _("Matches for you")
        email_message = self.email_messages.create(
            sender=settings.MATRIMONY_SENDER_EMAIL,
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


class MaleManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(gender="M")


class Male(MatrimonyProfile):
    objects = money_manager(MaleManager())

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
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
        self.gender = "F"
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
