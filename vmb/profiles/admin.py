from django.contrib import admin
from .models import Person, Guru, Language, Qualification, Occupation


# Register your models here.

# Define admin class

class PersonInline(admin.TabularInline):
    model = Person.languages_known.through
    extra = 1
    verbose_name = 'Language'
    verbose_name_plural = 'Languages Known'

class PersonAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name','gender']}),
        ('SPIRITUAL QUOTIENT', {'fields': ['rounds_chanting',('s_status','guru')]}),
        ('BIRTH DETAILS', {'fields': [('dob','tob'),'birth_country',('birth_state','birth_city')]}),
        ('CURRENT LOCATION', {'fields': ['current_country',('current_state','current_city')]}),
        ('PHYSICAL APPEARANCE', {'fields': [('height','complextion')]})

    ]
    inlines = [PersonInline]



# Register the admin class with associated model 
admin.site.register(Person, PersonAdmin)



class GuruAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(Guru, GuruAdmin)

class LanguageAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(Language, LanguageAdmin)

class QualificationAdmin(admin.ModelAdmin):
    pass

admin.site.register(Qualification, QualificationAdmin)

class  OccupationAdmin(admin.ModelAdmin):
    pass

admin.site.register(Occupation, OccupationAdmin)