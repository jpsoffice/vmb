from django.db import models

GENDER_CHOICES = (("M", "Male"), ("F", "Female"), ("O", "Others"))

SIKSHA_STATUS_CHOICES = (
    ("A", "Aspiring"),
    ("S", "Shelter"),
    ("D1", "Harinam"),
    ("D2", "Brahmin"),
)
# Create your models here.
GURUS = (
    ('H.H. Atmanivedana Swami'),
    ('H.H. Bhaktivaibhava Swami'),
    ('H.H. Bhakti Bhrnga Govinda Swami'),
    ('H.H. Bhakti Caitanya Swami'),
    ('H.H. Bhakti Charu Swami'),
    ('H.H. Bhakti Dhira Damodara Swami'),
    ('H.H. Bhakti Gaurava Narayan Swami'),
    ('H.H. Bhakti Gauravani Goswami'),
    ('H.H. Bhakti Prabhupada-vrata Damodara Swami'),
    ('H.H. Bhakti Raghava Swami'),
    ('H.H. Bhakti Sundar Goswami'),
    ('H.H. Bhakti Vijnana Goswami'),
    ('H.H. Bhakti Vikasa Swami'),
    ('H.H. Bhaktivyasa Tirtha Swami'),
    ('H.H. Bhakti VV Narasimha Swami'),
    ('H.H. Bhakti-bhusana Swami'),
    ('H.H. Bhaktimarga Swami'),
    ('H.G. Bhurijana Das'),
    ('H.H. Bir Krsna Das Goswami'),
    ('H.G. Caitanya Candra Das'),
    ('H.G. Caitanya Candra Caran Das'),
    ('H.H. Candra Mukha Swami'),
    ('H.H. Candramauli Swami'),
    ('H.G. Caru Das'),
    ('H.H. Danavir Goswami'),
    ('H.H. Devamrita Swami'),
    ('H.H. Dhanvantari Swami'),
    ('H.G. H.H. Dhirasanta Das Goswami'),
    ('H.G. Drutakarma Das'),
    ('H.H. Giridhari Swami'),
    ('H.H. Giriraja Swami'),
    ('H.G. H.H. Gopaswami Das'),
    ('H.H. Gopal Krsna Goswami'),
    ('H.H. Guru Prasad Swami'),
    ('H.H. Hanumatpresaka Swami'),
    ('H.G. Harivilas Das'),
    ('H.G. H.H. Hrdayananda dasa Goswami'),
    ('H.H. Indradyumna Swami'),
    ('H.G. H.H. Janananda dasa Goswami'),
    ('H.H. Jayapataka Swami'),
    ('H.G. Jivananda Das'),
    ('H.H. Kadamba Kanana Swami'),
    ('H.G. Kalakantha Das'),
    ('H.H. Kavicandra Swami'),
    ('H.G. H.H. Kesava Bharati dasa Goswami'),
    ('H.G. Kratu Das'),
    ('H.G. Kripamoya Das'),
    ('H.H. Krsna Ksetra Swami'),
    ('H.H. Lokanath Swami'),
    ('H.G. Madhu Sevita Das'),
    ('H.H. Mahadyuti Swami'),
    ('H.G. Mahaman Das'),
    ('H.G. Mahatma Das'),
    ('H.H. Mahavisnu Swami'),
    ('H.G. Manonatha Das'),
    ('H.G. Matsya Avatara Das'),
    ('H.G. Medhavi Das'),
    ('H.G. Nanda Kumar Das'),
    ('H.H. Navayogendra Swami'),
    ('H.H. Niranjana Swami'),
    ('H.G. H.H. Partha Sarathi Das Goswami'),
    ('H.H. Prahladananda Swami'),
    ('H.H. Purushatraya Swami'),
    ('H.H. Radha Govinda Swami'),
    ('H.H. Radhanath Swami'),
    ('H.H. Rama Govinda Swami'),
    ('H.G. Ravindra Svarupa Das'),
    ('H.H. Romapada Swami'),
    ('H.H. Rtadhvaja Swami'),
    ('H.H. Sacinandana Swami'),
    ('H.G. Samik Rsi Das'),
    ('H.G. Sankarsana Das'),
    ('H.G. Satyadeva Das'),
    ('H.H. Sivarama Swami'),
    ('H.H. Smita Krsna Swami'),
    ('H.H. Subhaga Swami'),
    ('H.G. Suresvara Das'),
    ('H.H. Trivikrama Swami'),
    ('H.G. Vaisesika Das'),
    ('H.H. Varsana Swami'),
    ('H.H. Vedavyasapriya Swami'),
    ('H.G. Virabahu Das')
)

M_STATUS = (
    ("SGL", "Single"),
    ("ENG", "Engaged"),
    ("MRD", "Married"),
    ("SEP", "Separated"),
    ("DIV", "Divorced"),
    ("WID", "Widow")
)

class Person(models.Model):

    name = models.CharField(max_length=250)

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    s_status = models.CharField(max_length=1, choices=SIKSHA_STATUS_CHOICES)
    
    dob = models.DateField()
    
    guru = models.CharField(max_length=100, choices=GURUS)
    
    tob = models.TimeField()
    
    birth_place = models.Charfield()
    
    current_place = models.Charfield()
    
    languages_known = models.Charfield()
    
    height = models.PositiveIntegerField()
    
    qualification = models.CharField(max_length=50)
    
    occupation = models.CharField(max_length=50)
    
    income = models.IntegerField()
    
    rounds_chanting = models.IntegerField()
    
    marital_status = models.CharField(max_length=3, choices=M_STATUS)
    
    email_id = models.EmailField( blank=True, null=True, verbose_name=_("Email"))
    
    phone = CharField(
        max_length=17,
        verbose_name=_("Phone number"),
    )
    
    expectations = models.TextField(max_length=300)

    def age(self):
    if self.dob:
        return int((datetime.datetime.now() - self.dob).days / 365.25)

    def __str__(self):
        return self.name
