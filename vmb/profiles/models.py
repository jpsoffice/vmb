from django.db import models
from django.utils.translation import ugettext_lazy as _

GENDER_CHOICES = (("M", "Male"), ("F", "Female"), ("O", "Others"))

SIKSHA_STATUS_CHOICES = (
    ("A", "Aspiring"),
    ("S", "Shelter"),
    ("D1", "Harinam"),
    ("D2", "Brahmin"),
)
# Create your models here.
M_STATUS = (
    ("SGL", "Single"),
    ("ENG", "Engaged"),
    ("MRD", "Married"),
    ("SEP", "Separated"),
    ("DIV", "Divorced"),
    ("WID", "Widow")
)

class Person(models.Model):
    """Model representing a person"""
    name = models.CharField(
        max_length=200, verbose_name=_("Name"))
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    rounds_chanting = models.PositiveIntegerField(
        verbose_text=_('Rounds'), 
        help_text='How many rounds are you chanting?',
        default=0,
    )
    s_status = models.CharField(
        max_length=1, 
        help_text= 'Enter siksha status (e.g. Aspiring, Shelter etc.)' 
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

    #Birth City/Town, State and Country
    birth_city = models.Charfield(
        verbose_name=_('City'),
        help_text='Enter birth village/town/city'
    )
    birth_state = models.Charfield(verbose_name =_('State'))
    birth_country = models.Charfield(verbose_name =_('Country'))

    #Current village/town/city, State and Country
    current_city = models.Charfield(
        verbose_name=_('City'),
        help_text='Enter current village/town/city'
    )
    current_state = models.Charfield(verbose_name =_('State'))
    current_country = models.Charfield(verbose_name =_('Country'))
    
    languages_known = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)
    height = models.DecimalField(help_text='Height in cms', blank=True)
    qualification = models.ForeignKey('Qualification', help_text='H.S., Graduate etc.')
    occupation = models.ForeignKey('Occupation', help_text='Doctor, Engineer, Businessman etc.')
    annual_income = models.IntegerField(help_text='Enter income in a year')
    marital_status = models.CharField(
        max_length=3, choices=M_STATUS, help_text='Single, Divorced etc.'
    )
    
    email_id = models.EmailField( blank=True, null=True, verbose_name=_("Email"))
    phone = CharField(
        max_length=17, verbose_name=_("Phone number"),
    )
    
    def age(self):
    if self.dob:
        return int((datetime.datetime.now() - self.dob).days / 365.25)

    def __str__(self):
        return self.name

class Guru(models.Model):
    """Model for representing an Initiating Guru"""
    name = CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.name

class Language(models.Model):
    """Model representing a Language(e.g. Hindi, English, Gujrati etc.)"""
    name = CharField(max_length=255, unique=True, db_index=True verbose_name=_('Language'))
    code = CharField(max_length=3, unique=True, db_index=True, verbose_name=_('Language Code'))

    class Meta:
        db_table = "language"

    def __str__(self):
        return f'{self.name} {self.code}'

class Qualification(models.Model):
    """Model representing Qualification(e.g. Bachelor, Masters, Doctorate etc.)"""
    degree = CharField(max_length=255, unique=True, verbose_name=_("Qualification"))

    def __str__(self):
        return f'{self.degree}'

class Occupation(models.Model):
    """Model representing Occupation(e.g. Doctor, Engineer, Entrepreneur etc.)"""
    occupation = CharField(max_length=255, uniques=True)

    def __str__(self):
        return f'{self.occupation}'


