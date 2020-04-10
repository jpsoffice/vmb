import datetime
from admin_numeric_filter.admin import NumericFilterModelAdmin, SingleNumericFilter, \
    RangeNumericFilter, SliderNumericFilter
from django.contrib import admin
from .models import MatrimonyProfile, Guru, Language, Degree, Occupation


# Register your models here.

# Define admin class

class MatrimonyProfileInline(admin.TabularInline):
    model = MatrimonyProfile.languages_known.through
    extra = 1
    verbose_name = 'Language'
    verbose_name_plural = 'Languages Known'


class MatrimonyProfileAdmin(NumericFilterModelAdmin):
    fieldsets = [
        (None, {'fields': ['name',('gender','marital_status')]}),
        ('SPIRITUAL QUOTIENT', {'fields': ['rounds_chanting',('s_status','guru')]}),
        ('BIRTH DETAILS', {'fields': [('dob','tob'),'birth_country',('birth_state','birth_city')]}),
        ('CURRENT LOCATION', {'fields': ['current_country',('current_state','current_city')]}),
        ('PHYSICAL APPEARANCE', {'fields': [('height','complexion')]}),            
        ('QUALIFICATON', {'fields': ['degree', ('occupation', 'monthly_income')]}),
        ('CONTACT INFORMATION', {'fields': [('phone', 'email_id')]}),
    ]
    inlines = [MatrimonyProfileInline]
    list_display = ('name','age','dob','current_country','current_city','occupation','monthly_income','phone','email_id')
    list_filter = ('current_state','current_city',('monthly_income', RangeNumericFilter),'gender')
    search_fields = ['name','current_country__name','current_state','current_city','occupation__occupation','monthly_income','phone','email_id']

    
# Register the admin class with associated model 
admin.site.register(MatrimonyProfile, MatrimonyProfileAdmin)


