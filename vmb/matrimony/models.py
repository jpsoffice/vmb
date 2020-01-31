import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
# from djmoney.models.fields import MoneyField

GENDER_CHOICES = (("M", "Male"), ("F", "Female"), ("O", "Others"))

SIKSHA_STATUS_CHOICES = (
    ("A", "Aspiring"),
    ("S", "Shelter"),
    ("D1", "Harinam"),
    ("D2", "Brahmin"),
)

COMPLEXION_CHOICES = (
    ("I", "Light, Pale White"),
    ("II", "White, Fair"),
    ("III", "Medium, White to light brown"),
    ("IV", "Olive, moderate brown"),
    ("V", "Brown, dark brown"),
    ("VI", "Very dark brown to black"),
)
# Create your models here.
M_STATUS = (
    ("SGL", "Single"),
    ("ENG", "Engaged"),
    ("SEP", "Separated"),
    ("DIV", "Divorced"),
    ("WID", "Widow")
)

class MatrimonyProfile(models.Model):
    """Model representing matrimonial profile of a candidate"""
    name = models.CharField(
        max_length=200, verbose_name=_("Name"),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,)

    rounds_chanting = models.PositiveIntegerField(
        verbose_name=_('Rounds'), 
        help_text='How many rounds are you chanting?',
        default=0,
    )
    s_status = models.CharField(
        max_length=2, 
        help_text= 'Enter siksha status (e.g. Aspiring, Shelter etc.)',
        choices=SIKSHA_STATUS_CHOICES,
        verbose_name=_("Siksha Status"),
        blank=True,
    )
    guru = models.ForeignKey('Guru', on_delete=models.SET_NULL, null=True, blank=True)
    
    dob = models.DateField(
        help_text= 'Enter birth date as YYYY-MM-DD', 
        verbose_name=_("Birth Date")
    )
    tob = models.TimeField(
        help_text='Enter time HH:MM:SS in 24hr format', 
        verbose_name=_("Birth Time"),
    )

    #Birth details
    # ------------------------------------------------------------------------------------
    birth_city = models.CharField(
        max_length=200,
        verbose_name=_('City'),
        help_text='Enter birth village/town/city'
    )
    birth_state = models.CharField(max_length=200, verbose_name=_('State'))
    birth_country = models.ForeignKey(
        'Country', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name="birthCountry", 
        verbose_name=_("Country"),
    )

    #Current details
    current_city = models.CharField(
        max_length=200,
        verbose_name=_("City"),
        help_text='Enter current village/town/city'
    )
    current_state = models.CharField(max_length=200, verbose_name=_('State'))
    current_country = models.ForeignKey(
        'Country', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='currentCountry',
        verbose_name=_('Country'),
    )

    languages_known = models.ManyToManyField('Language', help_text='Add the language you know')
    
    height = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        help_text='Height in cms', 
        blank=True,
    )
    complexion = models.CharField(
        max_length=3, 
        help_text= 'Enter your complexion',
        choices=COMPLEXION_CHOICES,
        blank=True,        
    )

    degree = models.ForeignKey(
        'Degree',
        on_delete=models.SET_NULL, 
        null=True, 
        help_text='H.S., Graduate etc.'
    )
    occupation = models.ForeignKey(
        'Occupation',
        on_delete=models.SET_NULL, 
        null=True, 
        help_text= 'Surgeon, Computer Application Engineer, etc.',
    )
    annual_income = models.PositiveIntegerField()
    marital_status = models.CharField(
        max_length=3, choices=M_STATUS, help_text='Single, Divorced etc.'
    )
    
    email_id = models.EmailField(blank=True, null=True, verbose_name=_("Email"))
    phone = models.CharField(
        max_length=17, verbose_name=_("Phone number"),
    )
    
    expectations = models.TextField(max_length=300, null=True)
    
    #Admins
    user = models.ForeignKey(
        'User',
        on_delete=models.SET_NULL, 
        null=True,
    )

    def age(self):
        if self.dob:
            return int((datetime.datetime.now().date() - self.dob).days / 365.25)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "matrimony_profile"


class User(models.Model):
    name = models.CharField(_("Name of User"), blank=True, max_length=255)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})


class Guru(models.Model):
    """Model for representing an Initiating Guru"""
    name = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "guru"


class Country(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True, help_text=_("Name"))
    code = models.CharField(max_length=3, unique=True, db_index=True, help_text=_("Code"))
    nationality = models.CharField(
        max_length=255, unique=True, db_index=True, help_text=_("Nationality")
    )

    class Meta:
        db_table = "country"

    def __str__(self):
        return "{} ({})".format(self.name, self.code)


class Nationality(Country):
    class Meta:
        proxy = True

    def __str__(self):
        return self.nationality

class Language(models.Model):
    """Model representing a Language(e.g. Hindi, English, Gujrati etc.)"""
    name = models.CharField(
        max_length=255, 
        unique=True, 
        db_index=True, 
        verbose_name=_('Language')
    )
    code = models.CharField(
        max_length=3, 
        unique=True, 
        db_index=True, 
        verbose_name=_('Language Code')
    )

    class Meta:
        db_table = "language"

    def __str__(self):
        return f'{self.name} {self.code}'


class Degree(models.Model):
    """Model representing Degree(e.g. Bachelor, Masters, Doctorate etc.)"""
    degree = models.CharField(max_length=255, unique=True, verbose_name=_("Degree"))

    def __str__(self):
        return f'{self.degree}'

    class Meta:
        db_table = "degree"


class Occupation(models.Model):
    """Model representing Occupation(e.g. Doctor, Engineer, Entrepreneur etc.)"""
    occupation = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ['occupation']
        db_table = 'occupation'

    def __str__(self):
        return f'{self.occupation}'



