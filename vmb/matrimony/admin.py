from django.contrib import admin
from .models import MatrimonyProfile, Guru, Language, Degree, Occupation


# Register your models here.

# Define admin class

class MatrimonyProfileInline(admin.TabularInline):
    model = MatrimonyProfile.languages_known.through
    extra = 1
    verbose_name = 'Language'
    verbose_name_plural = 'Languages Known'


class AgeFilter(admin.SimpleListFilter):
    title = 'age'
    parameter_name = 'age'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return [
            ('1', '<20'),
            ('2.1', '20-24'),
            ('2.2', '25-29'),
            ('3.1', '30-34'),
            ('3.2', '35-39'),
            ('4.1', '40-44'),
            ('4.2', '45-49'),
            ('5', '>=50'),            
        ]

    def queryset(self, request, queryset):

        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value() == '1':
            return queryset.filter(MatrimonyProfile.age()<20)
        if self.value() == '2.1':   
            return queryset.filter(MatrimonyProfile.age()>=20, MatrimonyProfile.age()<=24)
        if self.value() == '2.2':
            return queryset.filter(MatrimonyProfile.age()>=25, MatrimonyProfile.age()<=29)
        if self.value() == '3.1':
            return queryset.filter(MatrimonyProfile.age()>=30, MatrimonyProfile.age()<=34)
        if self.value() == '3.2':
            return queryset.filter(MatrimonyProfile.age()>=35, MatrimonyProfile.age()<=39)
        if self.value() == '4.1':
            return queryset.filter(MatrimonyProfile.age()>=40, MatrimonyProfile.age()<=44)                            
        if self.value() == '4.2':
            return queryset.filter(MatrimonyProfile.age()>=45, MatrimonyProfile.age()<=49)
        if self.value() == '5':
            return queryset.filter(MatrimonyProfile.age()>=50)            
        return queryset


class MatrimonyProfileAdmin(admin.ModelAdmin):
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
    list_filter = ('current_state','current_city','monthly_income','gender', AgeFilter)
    search_fields = ['name','current_country__name','current_state','current_city','occupation__occupation','monthly_income','phone','email_id']


# Register the admin class with associated model 
admin.site.register(MatrimonyProfile, MatrimonyProfileAdmin)


