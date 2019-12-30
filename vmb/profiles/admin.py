from django.contrib import admin
from .models import Person, Guru, Language, Degree, Occupation


# Register your models here.

# Define admin class

class PersonInline(admin.TabularInline):
    model = Person.languages_known.through
    extra = 1
    verbose_name = 'Language'
    verbose_name_plural = 'Languages Known'

class PersonAdmin(admin.ModelAdmin):

    fieldsets = [
        (None, {'fields': ['name',('gender','marital_status')]}),
        ('SPIRITUAL QUOTIENT', {'fields': ['rounds_chanting',('s_status','guru')]}),
        ('BIRTH DETAILS', {'fields': [('dob','tob'),'birth_country',('birth_state','birth_city')]}),
        ('CURRENT LOCATION', {'fields': ['current_country',('current_state','current_city')]}),
        ('PHYSICAL APPEARANCE', {'fields': [('height','complexion')]}),            
        ('QUALIFICATON', {'fields': ['degree', ('occupation', 'annual_income')]}),
        ('CONTACT INFORMATION', {'fields': [('phone', 'email_id')]}),
    ]
    inlines = [PersonInline]



# Register the admin class with associated model 
admin.site.register(Person, PersonAdmin)


